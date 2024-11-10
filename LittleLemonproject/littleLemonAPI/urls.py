from django.urls import path
from . import views

urlpatterns = [
    # Menu-items endpoints
    path('menu-items/',views.menu_items,name='menu-items'),
    # /api/menu-items/{menuItem
    path('menu-items/<int:menuItem>',views.menu_item_details,name='menu-item-details'),
    # /api/groups/manager/users
    path('groups/manager/users/',views.managers_list),
    path('groups/manager/users/<int:userId>',views.managers_details),
    path('groups/delivery-crew/users/',views.delivery_crew_list),
    path('groups/delivery-crew/users/<int:userId>',views.delivery_crew_details),
    path('cart/menu-items/',views.cart_item_list),
    path('orders/',views.orders_list),
    path('orders/<int:orderId>',views.order_details),
    path('category/',views.category_list),
    path('category/<int:pk>',views.category_details),

    
]