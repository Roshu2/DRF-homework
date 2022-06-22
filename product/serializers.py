from asyncore import read
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
    username = serializers.SerializerMethodField()
    
    def get_username(self, obj):
        # user_list = [user.username for user in obj.author]
        # # last_user = user_list.append(obj.author.username)
        # print(user_list)
        return 
    
    class Meta:
        model = ReviewModel
        fields = ["username"]

class ProductSerializer(serializers.ModelSerializer):
    review = serializers.SerializerMethodField()
    review_author = ReviewSerializer(read_only=True, source="review_set", many=True)
    is_active = serializers.BooleanField(default=True)
    
    #최신 리뷰 1개만 불러오기
    def get_review(self, obj):
        reviews = list(obj.review_set.values())
        if len(reviews) == 0:
            return "리뷰 없음"
        return reviews[-1]
        
        
    
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
         
        
        if instance.updated_at == instance.created_date:
            instance.description = f"<{instance.updated_at} 에 수정됨> \n {instance.description}"
            instance.save()
        else:
            split_desc_list = instance.description.split("\\n")
            split_desc ="\n".join(split_desc_list[1:])
            updated_desc = f"<{instance.updated_at} 에 수정됨>\n{split_desc}"
            
            instance.description = updated_desc
            instance.save()
        return instance
            
            
            
    
    class Meta:
        model = ProductModel
        fields = ["seller", "title", "thumbnail", "description", 
                  "price", "average_review","review_author", "review", "is_active", "exposure_end", "exposure_start", "created_date", "updated_at"]