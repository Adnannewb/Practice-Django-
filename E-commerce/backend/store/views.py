from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product,Category,CartItem,Cart
from .serializers import ProductSerializer,CategorySerializer,CartSerializer,CartItemSerializer



# Create your views here.
@api_view(['GET'])
def get_categories(request):
    categories=Category.objects.all()
    serializer=CategorySerializer(categories,many=True)
    return Response(serializer.data)
@api_view(['GET'])
def get_products(request):
    products=Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_product(request, id=None):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    serializer = ProductSerializer(product,context={'request': request} )
    return Response(serializer.data)

@api_view(['GET'])
def get_cart(request):
    cart,created=Cart.objects.get_or_create(user=None)
    serializer=CartSerializer(cart)
    return Response(serializer.data)
@api_view(['POST'])
def add_to_cart(request):
    product_id=request.data.get('product_id')
    product=Product.objects.get(id=product_id)
    cart,created=Cart.objects.get_or_create(user=None)
    item,created=CartItem.objects.get_or_create(cart=cart,product=product)
    if not created:
        item.quantity+=1
        item.save()
    cart_serialized_data = CartSerializer(cart).data
    return Response({'message':'Product Added to Cart',"cart":cart_serialized_data})

@api_view(['POST'])
def update_cart_quantity(request):
    item_id=request.data.get('item_id')
    quantity=request.data.get('quantity')
    if not item_id or quantity is None:
        return Response({'error':'Item ID and quantity are required'})
    try:
        item=CartItem.objects.get(id=item_id)
        if int(quantity)<1:
            cart=item.cart
            item.delete()
        else:
            item.quantity=int(quantity)
            item.save()
            cart=item.cart
        return Response({'message':'Cart quantity updated successfully', 'cart':CartSerializer(cart).data})
    except CartItem.DoesNotExist:
        return Response({'error':'Item not found'})

@api_view(['POST'])
def remove_from_cart(request):
    item_id=request.data.get('item_id')
    item=CartItem.objects.filter(id=item_id).first()
    if item is None:
        return Response({'error':'Item not found'}, status=404)
    cart=item.cart
    item.delete()
    return Response({'message':'Item Removed from Cart', 'cart':CartSerializer(cart).data})

    