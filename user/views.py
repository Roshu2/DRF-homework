from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from blog.models import Article as ArticleModel


class UserView(APIView):
    permission_classes = [permissions.AllowAny]
    
     #사용자 정보 조회
    def get(self, request):
        user = request.user
        articles = ArticleModel.objects.filter(user_id=user.id).values()
        
        title_list = []
        for article in articles:
            title = article['title']
            title_list.append(title)
        
        title_list = ", ".join(title_list)
        
        return Response({"title": title_list})
    
    #회원 가입
    def post(self, request):
        
        return Response({"message": "회원가입 성공!!"})
    
    #회원 정보 수정
    def put(self, request):
        
        return Response({"message": "회원 정보 수정!!"})
    
    #회원 탈퇴
    def delete(self, request):
        
        return Response({"message": "회원 탈퇴!!"})
    
    
    
class UserAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    # 로그인
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."})

        login(request, user)
        return Response({"message": "로그인 성공!!"})
    
    #로그아웃
    def delete(self, request):
        logout(request)
        return Response({"message": "로그아웃 성공!"})
