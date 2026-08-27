from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAdminUser,AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def get_product(request):
    products=Product.objects.filter(is_active=True)
    
    # search part 
    search = request.query_params.get('search')
    if search:
        products=products.filter(name__icontains=search)
    
    #Filter by Category
    category=request.query_params.get('category')
    if category:
        products=products.filter(category__iexact=category)
    
    #Filter by minimum price 
    min_price=request.query_params.get('min_price')
    if min_price:
        products=products.filter(price__gte=min_price)
    
    #Filter by maximum price 
    max_price=request.query_params.get('max_price')
    if max_price:
        products=products.filter(price__lte=max_price)
    
    #Pagination
    paginator=PageNumberPagination()
    paginator.page_size=3
    result_page = paginator.paginate_queryset(products, request)

    serializer = ProductSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_product(request):
    serializer=ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'Product Added Successfully '})
    return Response(serializer.errors)

@api_view(['PUT','DELETE'])
@permission_classes([IsAdminUser])      
def edit_delete_product(request,pk):
    product=get_object_or_404(Product,pk=pk)
    if request.method=='PUT':
        serializer=ProductSerializer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method=='DELETE':
        product.delete()
        return Response({'message':'Product Deleted Successfully'})
    


