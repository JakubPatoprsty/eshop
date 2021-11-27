from django.urls import path
from store import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

]
