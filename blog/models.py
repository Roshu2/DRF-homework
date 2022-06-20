from datetime import timedelta, datetime
from django.utils import timezone
from django.db import models
from user.models import User as UserModel



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=256)
    
    def __str__(self):
        return self.name
    
class Article(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    category = models.ManyToManyField(Category, related_name="articles")
    content = models.TextField(max_length=255)
    show_article = models.DateTimeField(default=timezone.now() + timedelta(days=3))
    end_article = models.DateTimeField(default=timezone.now() + timedelta(days=10))
    
    def __str__(self):
        return f"{self.user.username} 님의 {self.title}게시글입니다."
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField("댓글", max_length=256)
    
    def __str__(self):
        return f"{self.article.user} 님의 게시글 {self.user.username} 님의 댓글"
    
