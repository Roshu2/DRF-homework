from pydoc import describe
from unicodedata import category
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
    
    def __str__(self):
        return f"{self.user.username} 님의 게시글입니다."
