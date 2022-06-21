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
        fields = ["name", "id"]
        
        
class CommentSerializer(serializers.ModelSerializer):  
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.username
    
    class Meta:
        model = CommentModel
        fields = ["user", "comment"]
   
        
class ArticleSerializer(serializers.ModelSerializer):  
    category = CategorySerializer(many=True, read_only=True)
    get_categories = serializers.ListField(required=False) # 프론트에서 list로 데이터 보내줄때 사용
    comments = CommentSerializer(many=True, source="comment_set", read_only=True)
    
    def validate(self, data):
        categories = data.get("get_categories", [])
        
        if len(data.get("title", "")) < 5 :
            raise serializers.ValidationError(
                detail={"error": "제목은 5글자 이상 적어주세요."}
            )
        if len(data.get("content", "")) < 20 :
            raise serializers.ValidationError(
                detail={"error": "내용은 20자 이상 적어주세요."}
            )
        if not categories:
            raise serializers.ValidationError(
                detail={"error": "카테고리를 선택 해주세요."}
            )
        for category_id in categories:
            if not CategoryModel.objects.filter(id=category_id).exists():
                raise serializers.ValidationError(
                detail={"error": "카테고리를 잘못 지정했습니다."}
            )
            # category의 존재 유무 try except 코드    
            # try:
            #     CategoryModel.objects.get(id=category_id)
            # except:
            #     raise serializers.ValidationError(
            #     detail={"error": "카테고리를 잘못 지정했습니다."}
            # )
    
        return data
    
    def create(self, validated_data):
        #mixed in, generic class? create의 구조가 바뀌는것 참고!
        
        get_categorys = validated_data.pop("get_categories")
        
        article = ArticleModel(**validated_data)
        article.save()
        article.category.add(*get_categorys)
        
        return article
    
    def update(self, instance, validated_data):
        get_categorys = validated_data.pop("get_categories")
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        instance.category.set(get_categorys)
        return instance
    
    class Meta:
        model = ArticleModel
        fields = ["category", "title", "content", "comments", "user", "get_categories"]

        
