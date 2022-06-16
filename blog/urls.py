from django.urls import path
from blog import views

urlpatterns = [
    #blog/
    path('', views.MyArticleView.as_view()),
]