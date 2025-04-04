from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    task_list, task_create, task_update, task_delete, 
    toggle_task_complete, delete_account, SignUpView
)

urlpatterns = [
    path('', task_list, name='task_list'),
    path('create/', task_create, name='task_create'),
    path('update/<int:task_id>/', task_update, name='task_update'),
    path('delete/<int:task_id>/', task_delete, name='task_delete'),
    path('task/<int:task_id>/toggle/', toggle_task_complete, name='task_toggle_complete'),

    # 🔑 회원가입, 로그인, 로그아웃
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('delete_account/', delete_account, name='delete_account'),
]
