from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from store import views
from store.views import RegistrationView
from store.views import ProductList
urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('products/', ProductList.as_view()),
    path('products/<int:pk>/', views.productdetail, name='product_detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout')
]
