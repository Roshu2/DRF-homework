from rest_framework import serializers
from blog.serializers import ArticleSerializer

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



class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birthday", "age"]
        
class UserSerializer(serializers.ModelSerializer):  
    userprofile = UserProfileSerializer()
    article_set = ArticleSerializer(many=True)
    
    class Meta:
        model = UserModel
        fields = ["username", "email", "fullname", "userprofile", "article_set"]