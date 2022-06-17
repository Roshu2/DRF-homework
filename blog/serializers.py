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
    comment_set = CommentSerializer(many=True)
    
    def get_category(self, obj):
        return [category.name for category in obj.category.all()]
    
    
    class Meta:
        model = ArticleModel
        fields = ["category", "title", "content", "comment_set"]