from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Product,Category,CartItem,Cart,Order,OrderItem
from .serializers import ProductSerializer,CategorySerializer,CartSerializer,CartItemSerializer
from django.contrib.auth.models import User
from django.db import transaction
from .serializers import UserSerializer,RegisterSerializer



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
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart,created=Cart.objects.get_or_create(user=request.user)
    serializer=CartSerializer(cart)
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id=request.data.get('product_id')
    if not product_id:
        return Response({'error':'Product ID is required'}, status=400)
    try:
        product=Product.objects.get(id=product_id)
    except (Product.DoesNotExist, ValueError, TypeError):
        return Response({'error':'Product not found'}, status=404)
    cart,created=Cart.objects.get_or_create(user=request.user)
    item,created=CartItem.objects.get_or_create(cart=cart,product=product)
    if not created:
        item.quantity+=1
        item.save()
    cart_serialized_data = CartSerializer(cart).data
    return Response({'message':'Product Added to Cart',"cart":cart_serialized_data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_cart_quantity(request):
    item_id=request.data.get('item_id')
    quantity=request.data.get('quantity')
    if not item_id or quantity is None:
        return Response({'error':'Item ID and quantity are required'}, status=400)
    try:
        quantity=int(quantity)
        if quantity < 1:
            item=CartItem.objects.get(id=item_id, cart__user=request.user)
            cart=item.cart
            item.delete()
        else:
            item=CartItem.objects.get(id=item_id, cart__user=request.user)
            item.quantity=quantity
            item.save()
            cart=item.cart
        return Response({'message':'Cart quantity updated successfully', 'cart':CartSerializer(cart).data})
    except (CartItem.DoesNotExist, ValueError, TypeError):
        return Response({'error':'Invalid quantity or item not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    item_id=request.data.get('item_id')
    item=CartItem.objects.filter(id=item_id, cart__user=request.user).first()
    if item is None:
        return Response({'error':'Item not found'}, status=404)
    cart=item.cart
    item.delete()
    return Response({'message':'Item Removed from Cart', 'cart':CartSerializer(cart).data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    data=request.data
    name=str(data.get('name', '')).strip()
    address=str(data.get('address', '')).strip()
    phone=str(data.get('phone', '')).strip()
    payment_method=data.get('payment_method', 'COD')
    if not name or not address:
        return Response({'error':'Name and address are required'}, status=400)
    if not phone.isdigit() or len(phone) != 10:
        return Response({'error':'Invalid phone number'}, status=400)
    if payment_method not in {'COD', 'Online Payment', 'Credit Card'}:
        return Response({'error':'Invalid payment method'}, status=400)

    with transaction.atomic():
        cart,created=Cart.objects.get_or_create(user=request.user)
        items=list(cart.items.select_related('product'))
        if not items:
            return Response({'error':'Cart is empty'}, status=400)
        total=sum(item.product.price * item.quantity for item in items)
        order=Order.objects.create(user=request.user, total_amount=total)
        OrderItem.objects.bulk_create([
            OrderItem(order=order, product=item.product,
                      quantity=item.quantity, price=item.product.price)
            for item in items
        ])
        cart.items.all().delete()
    return Response({"message":"Order Placed Successfully", "Order_Id":order.id})

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer=RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user=serializer.save()
        return Response({"message":"User Registered Successfully","user":UserSerializer(user).data})
    return Response(serializer.errors,status=400)

