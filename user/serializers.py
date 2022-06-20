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



class HobbySerializer(serializers.ModelSerializer):
    same_hobby_users = serializers.SerializerMethodField()
    
    def get_same_hobby_users(self, obj):
        user = self.context["request"].user
        
        return [up.user.username for up in obj.userprofile_set.exclude(user=user)]

    class Meta:
        model = HobbyModel
        fields = ["name", "same_hobby_users"]


class UserProfileSerializer(serializers.ModelSerializer):
    hobby = HobbySerializer(many=True)
    
    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birthday", "age", "hobby"]
        
        
class UserSerializer(serializers.ModelSerializer):  
    userprofile = UserProfileSerializer()
    articles = ArticleSerializer(many=True, source="article_set")
    login_user_username = serializers.SerializerMethodField()
    
    def get_login_user_username(self, obj):
        return self.context["request"].user.username
    
    class Meta:
        model = UserModel
        fields = ["username", "email", "fullname", "userprofile", "articles", "login_user_username"]