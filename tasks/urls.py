from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.task_list, name='task_list'),
    path('add/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.task_update, name='task_update'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chatbot/api/', views.chatbot_api, name='chatbot_api'),
]