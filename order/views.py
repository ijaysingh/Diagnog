import json
from django.shortcuts import render, get_object_or_404, redirect
from order.models import Order, OrderItem, coupon
from product.models import product

from user.models import ShippingAddress, myUser

# Create your views here.

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def cartPage(request):
    context = {}
    if is_ajax(request):
        action = request.GET.get('action')
        id = request.GET.get('id')
        if request.user.is_authenticated:
            email = request.user.email
            userID = myUser.objects.get(email=email)
            order, created = Order.objects.get_or_create(user=userID,complete = False)
            items = order.orderitem_set.all()
            obj = get_object_or_404(OrderItem, product = id)
            if action == 'remove':
                obj.delete()
            if action == 'add':
                order, created = Order.objects.get_or_create(user=userID,complete = False)
                orderItem, created = OrderItem.objects.get_or_create(order=order, product=obj.product)
                context['prod'] = obj.product
    return render(request, 'order/cart.html', context)


def update_cart(request):
    id = request.GET.get('id')
    quantity = request.GET.get('quantity')
    if request.user.is_authenticated:
        email = request.user.email
        userid = myUser.objects.get(email=email)
        clickedProduct = product.objects.get(id=id)
        order = Order.objects.get(user=userid,complete = False)
        orderItem = OrderItem.objects.get(order=order, product=clickedProduct)
        if quantity<='0':
            orderItem.delete()
        else:
            orderItem.quantity = quantity
            orderItem.save()
    return render(request, 'order/cart.html')

def trackOrder(request):
    return render(request, 'order/order_tracking.html')
