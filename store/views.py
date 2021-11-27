from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from django.views.generic import ListView
from .models import *
from .utils import cookieCart, cartData, guestOrder


def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

class ProductList(ListView):
    model = Product

def productdetail(request,id):
    product = Product.objects.get(id = id)
    return render(request, 'store/detail.html', {'product': product})


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

from store.forms.auth import RegistrationForm


#####################
# Class based views #
#####################


class LogoutView(View):
    """
    NOTE: Django has built it LogoutView (from django.contrib.auth.views import LogoutView)
    but this django LogoutView expect us to have logout template.

    In our case we will have LogoutView in the base template. So we implement it ourselves.
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('homepage')


class LoginView(FormMixin, TemplateView):
    """
    NOTE: Django has built it LoginView (from django.contrib.auth.views import LoginView).

    Reason why I'm not using it is that I wanted to explain how is it done under the hood
    """
    template_name = 'accounts/templates/registration/login.html'
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Log in successfully')
            return redirect('homepage')

        messages.error(request, 'Wrong credentials')
        return redirect('auth:login')


class RegistrationView(FormMixin, TemplateView):
    template_name = 'accounts/registration.html'
    form_class = RegistrationForm

    def post(self, request,  *args, **kwargs):
        registration_data = request.POST
        form = self.form_class(registration_data)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account {form.cleaned_data.get("username")} successfully created')
            return redirect('auth:login')
        else:
            messages.error(request, f'Something wrongs')
            return TemplateResponse(request, 'accounts/registration.html', context={'form': form})


########################
# Function based views #
########################


def logout_view(request):
    logout(request)

def login_view(request):
    if request.method == 'GET':
        context = {
            'form': AuthenticationForm(),
        }
        return TemplateResponse(request, 'accounts/templates/registration/login.html', context=context)

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Log in successfully')
            return redirect('homepage')

        messages.error(request, 'Wrong credentials')
        return redirect('auth:login')


def registration_view(request):
    if request.method == 'GET':
        context = {
            'form': RegistrationForm(),
        }
        return TemplateResponse(request, 'accounts/registration.html', context=context)

    elif request.method == 'POST':
        registration_data = request.POST
        form = RegistrationForm(registration_data)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account {form.cleaned_data.get("username")} successfully created')
            return redirect('auth:login')
        else:
            messages.error(request, f'Something wrongs')
            return TemplateResponse(request, 'accounts/registration.html', context={'form': form})

