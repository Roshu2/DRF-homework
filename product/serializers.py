from importlib.resources import read_binary
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

from product.models import Product as ProductModel, Review as ReviewModel
from django.utils import timezone



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = ["author", "content", "rating"]

class ProductSerializer(serializers.ModelSerializer):
    review = serializers.SerializerMethodField()
    
    is_active = serializers.BooleanField(default=True)
    
    #최신 리뷰 1개만 불러오기
    def get_review(self, obj):
        reviews = list(obj.review_set.values())
        if len(reviews) == 0:
            return "리뷰엄슴"
        return reviews[-1]["content"]
        
        
    
    average_review = serializers.SerializerMethodField()
    
    #상품의 평점 평균을 불러오는 함수
    def get_average_review(self, obj):
        product_reviews = obj.review_set.values()
        rating_list = [review['rating'] for review in product_reviews]
    
        if len(rating_list) == 0:
            average_rating = "평점 없음"
        else:    
            average_rating = round(sum(rating_list) / len(rating_list), 1) #round 는 반올림. 뒤에 1은 소숫점 1자리만 보임.2면 2자리
            
        
        return average_rating
    
    def validate(self, data):
        http_method = self.context.get("request").method
        if http_method == "POST":
            if data.get("exposure_end") < timezone.now():
                raise serializers.ValidationError(
                    detail={"error": "상품 등록기간이 끝났습니다!"}
                )
        return data
    
    def create(self, validated_data):
        product = ProductModel(**validated_data)
        product.save()
        product.description += f"  <{product.created_date} 에 등록된 상품입니다.>"
        product.save()
        
        
        return product
    
    def update(self, instance, validated_data):
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        instance.description = f"<{instance.updated_at} 에 수정됨> "+ instance.description
        instance.save()
        
        return instance
    
    class Meta:
        model = ProductModel
        fields = ["seller", "title", "thumbnail", "description", 
                  "price", "average_review", "review", "is_active", "exposure_end", "exposure_start"]