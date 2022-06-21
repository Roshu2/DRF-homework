from django.urls import path
from user import views

urlpatterns = [
    #user/
    path('', views.UserView.as_view()),
    path('login/', views.UserAPIView.as_view()),
    path('logout/', views.UserAPIView.as_view()),
    path('<obj_id>/', views.UserView.as_view()),
]