from rest_framework.permissions import BasePermission
from datetime import timedelta
from django.utils import timezone

class RegistedMoreThanThreeDaysUser(BasePermission):
    
    message = '가입 후 3일 이상 지난 사용자만 사용하실 수 있습니다.'
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.join_date < (timezone.now() - timedelta(minutes=3)))