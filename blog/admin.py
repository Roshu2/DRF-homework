from django.contrib import admin
from .models import Category as CategoryModel, Article as ArticleModel, Comment as CommentModel

admin.site.register(CategoryModel)
admin.site.register(ArticleModel)
admin.site.register(CommentModel)

