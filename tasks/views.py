from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from groq import Groq
import os
import json
def home(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    return render(request, 'tasks/home.html')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    search_query = request.GET.get('q', '')
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    status_filter = request.GET.get('status', '')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    all_tasks = Task.objects.filter(user=request.user)
    today = timezone.now().date()

    stats = {
        'total': all_tasks.count(),
        'done': all_tasks.filter(status='done').count(),
        'pending': all_tasks.filter(status='pending').count(),
        'overdue': all_tasks.filter(due_date__lt=today).exclude(status='done').count(),
    }

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'search_query': search_query,
        'status_filter': status_filter,
        'stats': stats,
        'today': today,
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/signup.html', {'form': form})

def get_groq_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))


@login_required
def chatbot(request):
    return render(request, 'tasks/chatbot.html') #



@login_required
def chatbot_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        tasks = Task.objects.filter(user=request.user)
        tasks_text = ""
        for task in tasks:
            tasks_text += f"- {task.title} | الحالة: {task.get_status_display()} | الأولوية: {task.get_priority_display()}"
            if task.due_date:
                tasks_text += f" | تاريخ الاستحقاق: {task.due_date}"
            tasks_text += "\n"

        if not tasks_text:
            tasks_text = "لا توجد مهام حالياً."

        today = timezone.now().date()

        classify_prompt = f"""
حلل رسالة المستخدم التالية وحدد هل هو يطلب إضافة مهمة جديدة أو يسأل سؤال عادي.

التاريخ اليوم: {today}

رسالة المستخدم: "{user_message}"

إذا كان يطلب إضافة مهمة، رد بصيغة JSON فقط بدون أي نص إضافي، بهذا الشكل بالضبط:
{{"action": "add_task", "title": "عنوان المهمة", "priority": "high أو low", "due_date": "YYYY-MM-DD أو null"}}

إذا كان سؤال عادي (مو طلب إضافة)، رد بصيغة JSON فقط بدون أي نص إضافي، بهذا الشكل بالضبط:
{{"action": "question"}}

رد بـ JSON فقط، بدون أي شرح أو نص قبله أو بعده.
"""

        try:
            client = get_groq_client()

            classify_response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": classify_prompt}],
            )
            classify_text = classify_response.choices[0].message.content.strip()

            classify_text = classify_text.replace('```json', '').replace('```', '').strip()
            result = json.loads(classify_text)

            if result.get('action') == 'add_task':
                new_task = Task.objects.create(
                    title=result.get('title', 'مهمة جديدة'),
                    priority=result.get('priority', 'low'),
                    due_date=result.get('due_date') if result.get('due_date') != 'null' else None,
                    user=request.user,
                    status='pending'
                )
                reply = f"✅ تمام! ضفت لك مهمة \"{new_task.title}\""
                if new_task.due_date:
                    reply += f" بتاريخ {new_task.due_date}"
                if new_task.priority == 'high':
                    reply += " وحطيتها عاجلة"
                return JsonResponse({'reply': reply})

            else:
                prompt = f"""
أنت مساعد ذكي لمستخدم بنظام إدارة مهام. أجب على أسئلته بالعربية الفصحى البسيطة فقط.

مهام المستخدم الحالية:
{tasks_text}

قواعد صارمة:
- اكتب بالعربية فقط، ممنوع أي لغة أخرى غير العربية والإنجليزية
- إذا استخدمت مصطلح إنجليزي، ضعه بين قوسين منفصل عن الجملة العربية
- كن مختصراً ومباشراً

سؤال المستخدم: {user_message}
"""
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}],
                )
                reply = response.choices[0].message.content
                return JsonResponse({'reply': reply})

        except Exception as e:
            return JsonResponse({'reply': f'صار خطأ: {str(e)}'})

    return JsonResponse({'reply': 'طلب غير صحيح'})