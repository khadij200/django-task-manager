from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('in_progress', 'جاري العمل'),
        ('done', 'منجز'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'عادي'),
        ('high', 'عاجل'),
    ]

    title = models.CharField(max_length=200) #عنوان المهمة
    description = models.TextField(blank=True) #وصف المهمة
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') #حالة المهمة
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low') #الأولوية
    due_date = models.DateField(null=True, blank=True)#تاريخ الاستحقاق
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')#ربط المهمة بالمستخدم

    def __str__(self): #يعرض عنوان المهمة بدل اسم تقني
        return self.title