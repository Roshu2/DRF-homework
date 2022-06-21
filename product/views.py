
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from product.models import Product as ProductModel
from product.serializers import ProductSerializer
from django.db.models import Q
from django.utils import timezone

class ProductView(APIView):
    # permission_classes = [IsAdminOrIsAuthenticatedReadOnly]
    
    #상품 조회
    def get(self, request):
        user = request.user
        products = ProductModel.objects.filter(
            Q(exposure_end__gte=timezone.now(), 
            exposure_start__lte=timezone.now()) | Q(seller=user)
            )
        
        product_serializer = ProductSerializer(products, many=True).data
        
        return Response(product_serializer, status=status.HTTP_200_OK)
    
    #상품 등록
    def post(self, request):
        seller = request.user
        request.data['seller'] = seller.id
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
