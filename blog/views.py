from unicodedata import category
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from blog.models import Article as ArticleModel, Category as CategoryModel
from ai.permissions import RegistedMoreThanWeekUser, IsAdminOrIsAuthenticatedReadOnly
from datetime import timedelta
from django.utils import timezone
from blog.serializers import ArticleSerializer
from django.db.models import Q

class ArticleView(APIView):
    # permission_classes = [IsAdminOrIsAuthenticatedReadOnly]
    #로그인한 사용자 게시글 제목
    def get(self, request):
        user = request.user
        articles = ArticleModel.objects.filter(
            Q(end_article__gte=timezone.now(), 
            show_article__lte=timezone.now())).order_by("-show_article")
        
        article_serializer = ArticleSerializer(articles, many=True).data
        
        return Response(article_serializer, status=status.HTTP_200_OK)
        
         
    #게시글 작성
    def post(self, request):
        user = request.user
        request.data['user'] = user.id
        
        # categorys = request.data.get('category', [])
        article_serializer = ArticleSerializer(data=request.data, context={"request": request})
        
        if article_serializer.is_valid(): # True or False 데이터가 유효한지 검사 
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)
        
        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # user = request.user
        # title = request.data.get('title', '')
        # categorys = request.data.get('category', [])
        # content = request.data.get('content', '')
        
        # if len(title) < 5 : 
        #     return Response({"제목은 5글자 이상!"}, status=status.HTTP_400_BAD_REQUEST)
        # if not categorys:
        #     return Response({"카테고리를 지정해주세요!"}, status=status.HTTP_400_BAD_REQUEST)
        # if len(content) < 20 :
        #     return Response({"내용은 20자 이상 써주세요!"}, status=status.HTTP_400_BAD_REQUEST)
        
        # article = ArticleModel(user=user, title=title, content=content)
        # article.save()
        # article.category.add(*categorys)
        
        
        # return Response({"title" : title, "category" : categorys, "content" : content}, status=status.HTTP_200_OK)
    
    #게시글 수정
    def put(self, request, obj_id):
        article = ArticleModel.objects.get(id=obj_id)
        article_serializer = ArticleSerializer(article, data=request.data, partial=True, context={"request": request}) #partial 을 쓰면 일부의 데이터만 넣을 수 있다.
        article_serializer.is_valid()
        article_serializer.save()
        return Response(article_serializer.data, status=status.HTTP_200_OK)
        

    #게시글 삭제
    def delete(self, request):
        
        return Response({"message": "게시글 삭제!!"})
    

        
        
    
