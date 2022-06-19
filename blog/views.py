from unicodedata import category
from rest_framework.views import APIView
# from rest_framework import permissions
from rest_framework.response import Response
from blog.models import Article as ArticleModel, Category as CategoryModel
from ai.permissions import RegistedMoreThanThreeDaysUser
# from blog.serializers import PostArticleSerializer

class MyArticleView(APIView):
    permissions_classes = [RegistedMoreThanThreeDaysUser]
    #로그인한 사용자 게시글 제목
    def get(self, request):
        user = request.user.id
        articles = ArticleModel.objects.filter(user_id=user).values()
        
        title_list = []
        for article in articles:
            title = article['title']
            title_list.append(title)
        
        title_list = ", ".join(title_list)
        
        return Response({"title": title_list})
    
    def post(self, request):
        user = request.user
        title = request.data.get('title', '')
        category = request.data.get('category', '')
        content = request.data.get('content', '')
        categorie = CategoryModel.objects.get(name=category)
        
        if len(title) < 5 : 
            return Response({"제목은 5글자 이상!"})
        elif category == '':
            return Response({"카테고리를 지정해주세요!"})
        elif len(content) < 20 :
            return Response({"내용은 20자 이상 써주세요!"})
        
        article = ArticleModel.objects.create(user=user, title=title, content=content)
        article.category.add(categorie)
        
        return Response({"title" : title, "category" : category, "content" : content})
        
        # print(user)
        # serializer = PostArticleSerializer(data=request.data)
        # print(serializer)
        
        # if serializer.is_valid(raise_exception=True) : # raise_exception=True를 통해 밑에 저장 실패 부분을 대신할 수 있음
        #     serializer.save(user_id=user) # 데이터베이스에 저장
        
        #     return Response(serializer.validated_data)
        

    
    

        
        
    
