from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'slug']



class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
       


class CartSerializer(serializers.ModelSerializer):
    menuitem = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    unit_price = serializers.DecimalField(max_digits=6,decimal_places=2, read_only=True)
    class Meta:
        model = Cart
        fields = ['id','menuitem','quantity','unit_price','price']
        read_only_fields = ['price']

    def create(self, validated_data):
        #set the unit price from the selected menu item
        menuitem = validated_data['menuitem']
        validated_data['unit_price'] = menuitem.price
        return super().create(validated_data)
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem,
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'