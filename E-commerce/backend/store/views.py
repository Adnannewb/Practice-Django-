from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Product,Category,CartItem,Cart,Order,OrderItem
from .serializers import ProductSerializer,CategorySerializer,CartSerializer,CartItemSerializer
from django.contrib.auth.models import User
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
    product=Product.objects.get(id=product_id)
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
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    item_id=request.data.get('item_id')
    item=CartItem.objects.filter(id=item_id).first()
    if item is None:
        return Response({'error':'Item not found'}, status=404)
    cart=item.cart
    item.delete()
    return Response({'message':'Item Removed from Cart', 'cart':CartSerializer(cart).data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    # try:
    #     data=request.data
        
    #     name=data.get('name')
    #     address=data.get('address')
    #     phone=data.get('phone')
    #     payment_method=data.get('payment_method','COD')
    #     cart=Cart.objects.first()
        
    #     if not cart or not cart.items.exists():
    #         return Response({'error':'Cart is empty'},status=400)
    #     total=sum(item.product.price * item.quantity for item in cart.items.all())
        
    #     #create order
    #     order=Order.objects.create(
    #         user=None,
    #         total_amount=total,
    #     )
        
    #     #create order item
    #     for item in cart.items.all():
    #         OrderItem.objects.create(
    #             order=order,
    #             product=item.product,
    #             quantity=item.quantity,
    #             price=item.product.price,
    #         )

    #     cart.items.all().delete()
    #     return Response({
    #         "message":"Order Placed Successfully",
    #         "Order_Id":order.id,
    #     })
    # except Exception as e:
        # return Response({"error":str(e)},status=500)
    try:
        data=request.data
        name=data.get('name')
        address=data.get('address')
        phone=data.get('phone')
        payment_method=data.get('payment_method','COD')
        
        #validate phone
        if not phone.isdigit() or len(phone)!=10:
            return Response({'error':'Invalid phone number'},status=400)
        
        cart,created=Cart.objects.get_or_create(user=request.user)
        
        if not cart or not cart.items.exists():
            return Response({'error':'Cart is empty'},status=400)
        total=sum(item.product.price * item.quantity for item in cart.items.all())
        
        #create order
        order=Order.objects.create(
            user=request.user,
            total_amount=total,
        )
        
        #create order item
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        cart.items.all().delete()
        return Response({
            "message":"Order Placed Successfully",
            "Order_Id":order.id,
        }) 
    except Exception as e:
        return Response({"error":str(e)},status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer=RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user=serializer.save()
        return Response({"message":"User Registered Successfully","user":UserSerializer(user).data})
    return Response(serializer.errors,status=400)

