from django.urls import path
from store import views
from store.views import ProductList, productdetail

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('products/', ProductList.as_view()),
    path('products/<int:pk>/', views.productdetail, name='product_detail'),
]
