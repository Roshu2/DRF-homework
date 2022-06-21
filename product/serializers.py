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

from product.models import Product as ProductModel


class ProductSerializer(serializers.ModelSerializer):
    
    
    def validate(self, data):
        
        return data
    
    def create(self, validated_data):
        product = ProductModel(**validated_data)
        product.save()
        
        return product
    
    def update(self, instance, validated_data):
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
    
        return instance
    
    class Meta:
        model = ProductModel
        fields = "__all__"