from datetime import datetime
from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from .models import MenuItem, Cart, Order, Category, OrderItem
from rest_framework.response import Response
from .serializers import MenuSerializer,CategorySerializer, OrderSerializer, UserSerializer, CartSerializer
from rest_framework import status
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated



# Create your views here.
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def category_list(request):
    if request.method == 'GET':
        items = Category.objects.all()
        serialized_items = CategorySerializer(items,many=True)
        return Response(serialized_items.data,status=status.HTTP_200_OK)
    if request.method == 'POST':
        serialized_item = CategorySerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data,status=status.HTTP_201_CREATED)

@api_view(['DELETE','PUT','PATCH'])
@permission_classes([IsAuthenticated])
def category_details(request,pk):
    if request.method == 'DELETE':
        item = Category.objects.get(pk=pk)
        item.delete()
        return Response({"message":"Item deleted!"},status=status.HTTP_204_NO_CONTENT)
    if request.method == 'PUT':
        item = Category.objects.get(pk=pk)
        serialized_item = CategorySerializer(item,data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data,status=status.HTTP_202_ACCEPTED)
    if request.method == 'PATCH':
        item = Category.objects.get(pk=pk)
        serialized_item = CategorySerializer(item,data=request.data,partial=True)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data,status=status.HTTP_202_ACCEPTED)
    

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def menu_items(request):
    #print current user group
    # print(request.user.groups.all())

    #search, pagination, ordering
    search = request.query_params.get('search')
    perpage = request.query_params.get('perpage',default=2)
    page = request.query_params.get('page',default=1)
    ordering = request.query_params.get('ordering',default='id')

    
    if request.method == 'GET':
        items = MenuItem.objects.all()

        #search
        if search:
            items = items.filter(title__icontains=search)
        
        #ordering
        if ordering:
            items = items.order_by(ordering)

        #pagination
        paginator = Paginator(items,per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []

        serialized_items = MenuSerializer(items,many=True)
        return Response(serialized_items.data,status=status.HTTP_200_OK)
    if request.user.groups.filter(name='Manager').exists():
        if request.method == 'POST':
            serialized_item = MenuSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data,status=status.HTTP_201_CREATED)
    return Response({"message":"You are not allowed to perform this action!"},status=status.HTTP_403_FORBIDDEN)
    


@api_view(['GET','DELETE','PUT','PATCH'])
@permission_classes([IsAuthenticated])
def menu_item_details(request,menuItem):
    if request.method == 'GET':
        item = MenuItem.objects.get(pk=menuItem)
        serialized_item = MenuSerializer(item)
        return Response(serialized_item.data,status=status.HTTP_200_OK)
    if request.user.groups.filter(name='Manager').exists():
        if request.method == 'DELETE':
            item = MenuItem.objects.get(pk=menuItem)
            item.delete()
            return Response({"message":"item removed!"},status=status.HTTP_204_NO_CONTENT)
        if request.method == 'PUT':
            item = MenuItem.objects.get(pk=menuItem)
            serialized_item = MenuSerializer(item,data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data,status=status.HTTP_202_ACCEPTED)
        if request.method == 'PATCH':
            item = MenuItem.objects.get(pk=menuItem)
            serialized_item = MenuSerializer(item,data=request.data,partial=True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data,status=status.HTTP_202_ACCEPTED)
    return Response(status=status.HTTP_403_FORBIDDEN)

# managers_list
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def managers_list(request):
    if request.user.groups.filter(name='Manager').exists():
        if request.method == 'GET':
            manager_group = Group.objects.get(name='Manager')
            managers = manager_group.user_set.all()
            serialized_items = UserSerializer(managers, many=True)
            return Response(serialized_items.data,status=status.HTTP_200_OK)
        if request.method == 'POST':
            user = get_object_or_404(User, username = request.data['username'])
            managers = Group.objects.get(name='Manager')
            managers.user_set.add(user)
            serialized_item = UserSerializer(user)
            return Response(serialized_item.data, status=status.HTTP_201_CREATED)
    return Response({"message":"You are not allowed to perform this action!"},status=status.HTTP_403_FORBIDDEN)

#manager_details
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def managers_details(request,userId):
    if request.user.groups.filter(name='Manager').exists():
        user = get_object_or_404(User,pk=userId)
        manager_group = Group.objects.get(name='Manager')
        manager_group.user_set.remove(user)
        return Response({"message":"user removed from Manager list!"},status=status.HTTP_200_OK)
# delivery_crew_list
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def delivery_crew_list(request):
    if request.user.groups.filter(name='Manager').exists():
        if request.method == 'GET':
            delivery_crew_group = Group.objects.get(name='Delivery crew')
            delivery_crew_list = delivery_crew_group.user_set.all()
            serialized_items = UserSerializer(delivery_crew_list,many=True)
            return Response(serialized_items.data,status=status.HTTP_200_OK)
        if request.method == 'POST':
            user = get_object_or_404(User,username=request.data['username'])
            delevery_crew = Group.objects.get(name='Delivery crew')
            delevery_crew.user_set.add(user)
            serialized_item = UserSerializer(user)
            return Response(serialized_item.data,status=status.HTTP_201_CREATED)

#delivery crew details
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delivery_crew_details(request,userId):
    user = get_object_or_404(User,pk=userId)
    delivery_crew_group = Group.objects.get(name='Delivery crew')
    delivery_crew_group.user_set.remove(user)
    return Response({"message":"user removed from Delivery crew group!"},status=status.HTTP_200_OK)

# orders_list
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def orders_list(request):
    if request.method == 'GET':
        if request.user.groups.filter(name='Manager').exists(): #manager
            orders = Order.objects.all()
            serialized_orders = OrderSerializer(orders,many=True)
            return Response(serialized_orders.data,status=status.HTTP_200_OK)
        elif request.user.groups.filter(name='Delivery crew').exists(): #delivery crew
            orders = Order.objects.filter(delivery_crew=request.user)
            serialized_orders = OrderSerializer(orders,many=True)
            return Response(serialized_orders.data,status=status.HTTP_200_OK)
        else:         #customer
            orders = Order.objects.filter(user=request.user)
            serialized_orders = OrderSerializer(orders,many=True)
            return Response(serialized_orders.data,status=status.HTTP_200_OK)
    if request.method == 'POST':
        if request.user.group.filter(name='Manager').exists():
            pass
        elif request.user.group.filter(name='Delivery crew').exists():
            pass
        else:
            cart_items = Cart.objects.filter(user=request.user)
        order = Order.objects.create(user=request.user, status=False, date=datetime.date.today())
        total_price = 0
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price
            )
            total_price += cart_item.price
            order_item.save()
        
        order.total = total_price
        order.save()
        cart_items.delete()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# order_details
@api_view(['GET','DELETE','PUT','PATCH'])
@permission_classes([IsAuthenticated])
def order_details(request,orderId):
    try:
        order = Order.objects.get(pk= orderId)
    except FileNotFoundError:
        return Response({'error':'Order does not exist'},status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        return Response(order,status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'PUT':
        order.status = request.data['status']
        order.save()
        return Response(order,status=status.HTTP_202_ACCEPTED)
    if request.method == 'PATCH':
        order.status = request.data['status']
        order.save()
        return Response(order,status=status.HTTP_202_ACCEPTED)
    
    
#cart items
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def cart_item_list(request):
    if request.method == 'POST':
        serialized_item = CartSerializer(data=request.data)

        if serialized_item.is_valid():
            menuitem = serialized_item.validated_data['menuitem'].id

            try:
                menuitem = MenuItem.objects.get(pk=menuitem)
            except MenuItem.DoesNotExist:
                return Response({"error":"Menu item does not exist"},status=status.HTTP_404_NOT_FOUND)
            #set the unit price from the menu item and calculate the price
            serialized_item.validated_data['unit_price'] = menuitem.price
            serialized_item.validated_data['user'] = request.user
            cart_item = serialized_item.save()
            return Response(CartSerializer(cart_item).data,status=status.HTTP_201_CREATED)
        return Response(serialized_item.errors,status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        cart_items = Cart.objects.filter(user = request.user)
        serialized_items = CartSerializer(cart_items,many=True)
        return Response(serialized_items.data,status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        cart_items = Cart.objects.filter(user=request.user)
        if cart_items:
            cart_items.delete()
            return Response({"message":"Your cart has been emptied"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"You do not have a cart"},status=status.HTTP_400_BAD_REQUEST)
