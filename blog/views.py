from time import time
from unicodedata import category
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from blog.models import Article as ArticleModel, Category as CategoryModel
from ai.permissions import RegistedMoreThanWeekUser, IsAdminOrIsAuthenticatedReadOnly
from datetime import timedelta
from django.utils import timezone

class ArticleView(APIView):
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly, RegistedMoreThanWeekUser]
    #로그인한 사용자 게시글 제목
    def get(self, request):
        user = request.user
        articles = ArticleModel.objects.filter(
            end_article__lte=timezone.now() + timedelta(days=10), 
            show_article__gte=timezone.now() - timedelta(days=3)).order_by("-show_article").values()
        
        my_articles = [article for article in articles] #for문 축약
        # titles = ", ".join(titles) # 콤마로 리스트를 분리 ["1","2"] > "1,2"
        
        return Response({"articles": my_articles}, status=status.HTTP_200_OK)
    
    #게시글 작성
    def post(self, request):
        user = request.user
        title = request.data.get('title', '')
        categorys = request.data.get('category', [])
        content = request.data.get('content', '')
        
        if len(title) < 5 : 
            return Response({"제목은 5글자 이상!"}, status=status.HTTP_400_BAD_REQUEST)
        if not categorys:
            return Response({"카테고리를 지정해주세요!"}, status=status.HTTP_400_BAD_REQUEST)
        if len(content) < 20 :
            return Response({"내용은 20자 이상 써주세요!"}, status=status.HTTP_400_BAD_REQUEST)
        
        article = ArticleModel(user=user, title=title, content=content)
        article.save()
        article.category.add(*categorys)
        
        return Response({"title" : title, "category" : categorys, "content" : content}, status=status.HTTP_200_OK)

        

    
    

        
        
    
