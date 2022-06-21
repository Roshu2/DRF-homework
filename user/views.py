from functools import partial
from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from blog.models import Article as ArticleModel
from user.serializers import UserSerializer
from ai.permissions import RegistedMoreThanWeekUser, IsAdminOrIsAuthenticatedReadOnly


class UserView(APIView):
    # permission_classes = [IsAdminOrIsAuthenticatedReadOnly]
    
     #사용자 정보 조회
    def get(self, request):
        
        user_serializer = UserSerializer(request.user, context={"request": request}).data
        
        return Response(user_serializer, status=status.HTTP_200_OK)
    
    #회원 가입
    def post(self, request):
        user_serializer = UserSerializer(data=request.data, context={"request": request})
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
        # if문을 걸어서 else일때 event를 적용시키려면 아래의 코드 그렇지 않으면 간단하게 위코드
        # if user_serializer.is_valid():
        #     user_serializer.save()
        #     return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        # return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #회원 정보 수정
    def put(self, request, obj_id):
        user = request.user
        user_serializer = UserSerializer(user, data=request.data, partial=True, context={"request": request}) #partial 을 쓰면 일부의 데이터만 넣을 수 있다.
        user_serializer.is_valid()
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
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
