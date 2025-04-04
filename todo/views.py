from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils.timezone import now, timedelta
from django.views.generic import CreateView
from .models import Task
from .forms import TaskForm

# 🏠 메인 페이지 (할 일 목록 표시)
def task_list(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user).order_by('-created_at')  # 최신순 정렬
        current_time = now()
        warning_date = current_time + timedelta(days=3)
    else:
        tasks = []
        current_time = None
        warning_date = None

    return render(request, 'todo/task_list.html', {
        'tasks': tasks,
        'now': current_time,
        'warning_date': warning_date
    })

# ✅ 할 일 추가 (로그인 필요)
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
    return render(request, 'todo/task_form.html', {'form': form})

# ✅ 할 일 수정 (로그인 필요)
@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()  # ✅ 중복 저장 방지
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form})

# ✅ 할 일 삭제 (로그인 필요)
@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')

# ✅ 할 일 완료 상태 토글 (로그인 필요)
@login_required
def toggle_task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed  # 완료 상태 변경
    task.save()
    return redirect('task_list')

# ✅ 회원가입 (클래스 기반 뷰 - CBV)
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")  # 회원가입 후 로그인 페이지로 이동
    template_name = "registration/signup.html"

# ✅ 계정 삭제 (로그인 필요)
@login_required
def delete_account(request):
    user = request.user
    user.delete()  # ✅ 계정 삭제 후 로그아웃
    logout(request)
    return redirect("/")
