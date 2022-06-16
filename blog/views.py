from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from blog.models import Article as ArticleModel

class MyArticleView(APIView):
    permissions_classes = [permissions.IsAuthenticated]
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
        
        
        
    
