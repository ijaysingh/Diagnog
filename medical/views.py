from django.shortcuts import render
from order.models import Order, OrderItem
from product.models import product
from user.models import headerOffer, myUser, wishlist


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def home(request):
    context = {}
    try:
        slider = headerOffer.objects.filter(enable=True)
    except:
        slider = {}
    context['slider'] = slider
    if is_ajax(request):
        id = request.GET.get('id')
        addWishlist = request.GET.get('wishlist')
        clickedProduct = product.objects.get(id=id)
        quantity = request.GET.get('quantity')
        addCart = request.GET.get('cart')
        if request.user.is_authenticated:
            email = request.user.email
            userid = myUser.objects.get(email=email)
            if addWishlist:
                l = wishlist.objects.get_or_create(user=userid, product=clickedProduct)
            if addCart:
                order, created = Order.objects.get_or_create(user=userid,complete = False)
                orderItem, created = OrderItem.objects.get_or_create(order=order, product=clickedProduct)
                if quantity:
                    orderItem.quantity = quantity
                    orderItem.save()
        context['prod'] = clickedProduct
    return render(request, 'pages/index.html', context)

def login(request):
    return render(request, 'pages/login.html')

def error(request):
    return render(request, 'pages/error.html')


def register(request):
    return render(request, 'pages/register.html')

def aboutPage(request):
    return render(request, 'pages/about.html')

def contactPage(request):
    return render(request, 'pages/contact.html')

def privacyPolicyPage(request):
    return render(request, 'pages/privacy_policy.html')

def termsAndConditionsPage(request):
    return render(request, 'pages/terms_conditions.html')