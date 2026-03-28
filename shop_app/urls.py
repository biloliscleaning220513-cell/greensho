from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/new/', views.product_create, name='product_create'),
    path('product/<int:pk>/order/', views.place_order, name='place_order'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:pk>/confirm/', views.confirm_delivery, name='confirm_delivery'),
    path('product/<int:pk>/edit/', views.product_update, name='product_update'),
    path('register/', views.register, name='register'),
    path('category/new/', views.category_create, name='category_create'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'), 
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
]