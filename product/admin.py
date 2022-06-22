from django.contrib import admin
from .models import Product as ProductModel, Review as ReviewModel

admin.site.register(ProductModel)
admin.site.register(ReviewModel)

