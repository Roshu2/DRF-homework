
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from product.models import Product as ProductModel
from product.serializers import ProductSerializer
from django.db.models import Q
from django.utils import timezone
from ai.permissions import IsAdminOrThreeDaysPassedrOrReadOnly
from rest_framework.permissions import AllowAny
class ProductView(APIView):
    permission_classes = [IsAdminOrThreeDaysPassedrOrReadOnly]
    
    #상품 조회
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            products = ProductModel.objects.filter(
                Q(exposure_end__gte=timezone.now(), 
                is_active=True) | Q(seller=user)
                )
            
            product_serializer = ProductSerializer(products, many=True).data
        else:
            products = ProductModel.objects.filter(
                Q(exposure_end__gte=timezone.now(), 
                is_active=True)
                )
            product_serializer = ProductSerializer(products, many=True).data   
            
        return Response(product_serializer, status=status.HTTP_200_OK)
        
    
    #상품 등록
    def post(self, request):
        user = request.user
        request.data['seller'] = user.id
        product_serializer = ProductSerializer(data=request.data, context={"request": request})
        
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #상품 수정
    def put(self, request, obj_id):
        product = ProductModel.objects.get(id=obj_id)
        product_serializer = ProductSerializer(product, data=request.data, partial=True, context={"request": request})
        product_serializer.is_valid()
        product_serializer.save()
        return Response(product_serializer.data, status=status.HTTP_200_OK)
