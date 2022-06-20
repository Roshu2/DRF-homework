from asyncore import read
from unittest.util import _MAX_LENGTH, _MIN_END_LEN
from urllib.parse import MAX_CACHE_SIZE
from rest_framework import serializers

from blog.models import (
    Category as CategoryModel,
    Article as ArticleModel,
    Comment as CommentModel
    )

from user.models import (
    User as UserModel,
    UserProfile as UserProfileModel,
    Hobby as HobbyModel
)



class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CategoryModel
        fields = ["name"]
        
        
class CommentSerializer(serializers.ModelSerializer):  
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.username
    
    class Meta:
        model = CommentModel
        fields = ["user", "comment"]
   
        
class ArticleSerializer(serializers.ModelSerializer):  
    category = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, source="comment_set")
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.username
    
    def get_category(self, obj):
        return [category.name for category in obj.category.all()]
    
    
    class Meta:
        model = ArticleModel
        fields = ["category", "title", "content", "comments", "user"]
        

# class PostArticleSerializer(serializers.ModelSerializer):
#     title = serializers.CharField(max_length=70, min_length=5, default='')
#     category = serializers.CharField(max_length=100)
#     content = serializers.CharField(max_length=256, min_length=20, default='')
    
#     def create(self, validated_data):
#         return ArticleModel.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.category = validated_data.get('category', instance.category)
#         instance.content = validated_data.get('content', instance.content)
#         instance.save()
#         return instance
    
    
#     class Meta:
#         model = ArticleModel
#         fields = ["category", "title", "content"]