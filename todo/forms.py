from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task

# 📝 할 일(Task) 생성 폼
class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        label="마감 기한",
        widget=forms.DateInput(attrs={"type": "date", "class": "w-full p-2 border rounded"}),
        required=False
    )
    
    priority = forms.ChoiceField(
        choices=Task.PRIORITY_CHOICES,  # ✅ 우선순위 선택 필드 추가
        label="우선순위",
        widget=forms.Select(attrs={"class": "w-full p-2 border rounded"})
    )

    completed = forms.BooleanField(
        label="완료 여부",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "w-5 h-5"})
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'completed']

# 🔑 회원가입 폼 (커스텀)
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="사용자 이름",
        widget=forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
        help_text="필수 입력 항목입니다. 150자 이하의 문자, 숫자, @/./+/-/_ 만 사용할 수 있습니다."
    )
    password1 = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(attrs={"class": "w-full p-2 border rounded"}),
        help_text="비밀번호는 최소 8자 이상이어야 합니다."
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(attrs={"class": "w-full p-2 border rounded"}),
        help_text="동일한 비밀번호를 입력하세요."
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")
        return password1  # Django 기본 비밀번호 검사를 통과하도록 수정
