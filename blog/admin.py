from django.contrib import admin
from .models import Category as CategoryModel, Article as ArticleModel

admin.site.register(CategoryModel)
admin.site.register(ArticleModel)

