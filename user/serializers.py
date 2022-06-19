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
        user_list = []
        for user_profile in obj.userprofile_set.all():
            user_list.append(user_profile.user.username)

        return user_list

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
    article_set = ArticleSerializer(many=True)
    
    class Meta:
        model = UserModel
        fields = ["username", "email", "fullname", "userprofile", "article_set"]