from datetime import timedelta, datetime
from django.utils import timezone
from django.db import models
from user.models import User as UserModel
from django.utils import timezone
from datetime import timedelta

class Product(models.Model):
    seller = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=70)
    thumbnail = models.ImageField("썸네일")
    description = models.TextField("설명", max_length=255, blank=True, null=True)
    created_date = models.DateField("작성일", auto_now_add=True)
    exposure_start = models.DateTimeField("노출 시작일", default=timezone.now)
    exposure_end = models.DateTimeField("노출 종료일", default=timezone.now() + timedelta(days=7))
    
    def __str__(self):
        return f"{self.author}님의 {self.title} 상품"
