from django.urls import path
from product import views

urlpatterns = [
    #product/
    path('', views.ProductView.as_view()),
    path('<obj_id>/', views.ProductView.as_view()),
]