from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    # 우선순위 선택 옵션 정의
    PRIORITY_CHOICES = [
        ('high', '🔴 높음'),
        ('medium', '🟠 중간'),
        ('low', '🟢 낮음'),
    ]

    title = models.CharField(max_length=255)  # 할 일 제목
    description = models.TextField(blank=True)  # 설명 (선택 사항)
    completed = models.BooleanField(default=False)  # 완료 여부
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 날짜 (자동 설정)
    updated_at = models.DateTimeField(auto_now=True)  # 수정 날짜
    due_date = models.DateField(null=True, blank=True, default=None)  # 마감 기한 (선택 사항)
    priority = models.CharField(  # ✅ 우선순위 필드 추가
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자 정보 (연결된 계정)

    class Meta:
        ordering = ['-created_at', 'completed']  # ✅ 최신순 + 미완료된 항목이 위로

    def __str__(self):
        return f"{self.title} ({self.get_priority_display()})"
