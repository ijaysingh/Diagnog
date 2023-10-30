from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from order.models import Order, OrderItem
from user.models import myUser, wishlist
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import PasswordResetForm
from .models import ShippingAddress, myUser as User
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import update_session_auth_hash
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from user.models import myUser, wishlist
# Create your views here.


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required(login_url='/login')
def showWishlist(request):
    email = request.user.email
    userID = myUser.objects.get(email=email)
    context = {}
    if is_ajax(request):
        action = request.GET.get('action')
        id = request.GET.get('id')
        obj = get_object_or_404(wishlist, product = id)
        if action == 'remove':
            obj.delete()
        if action == 'add':
            order, created = Order.objects.get_or_create(user=userID,complete = False)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=obj.product)
            context['prod'] = obj.product
    products = wishlist.objects.filter(user=userID)
    context['wishlist'] = products
    return render(request, 'user/wishlist.html', context)

def profile(request):
    if not request.user.is_authenticated:
        return HttpResponse('Please login first...')
    orders = Order.objects.filter(complete=True)
    email = request.user.email
    customer = myUser.objects.get(email=email)
    addresses = ShippingAddress.objects.filter(inactive=False).filter(user=customer)
    addressId = int(request.GET.get('addressId','-1'))
    action = request.GET.get('action')
    print(addressId)
    if action == "remove":
        addr = ShippingAddress.objects.get(id=addressId)
        addr.inactive = True
        addr.save()
    context = {
        'orders': orders,
        'addresses': addresses
    }
    return render(request,'user/profile.html', context)
    

def addAddress(request):
    email = request.user.email
    customer = myUser.objects.get(email=email)
    if request.method == 'POST':
        name = request.POST.get("name")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        street = request.POST.get("street")
        apartment = request.POST.get("apartment")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip = request.POST.get("zip")
        newAddress = ShippingAddress(user=customer, first_name=name, last_name=lastname, email=email, phone=phone, street_address=street, apartment_address=apartment, city=city, state=state, zip=zip)
        newAddress.save()
    orders = Order.objects.filter(complete=True)
    addresses = ShippingAddress.objects.filter(inactive=False).filter(user=customer)
    context = {
        'orders': orders,
        'addresses': addresses
    }
    return render(request,'user/profile.html', context)

def updateAddress(request,id):
    email = request.user.email
    customer = myUser.objects.get(email=email)
    if request.method == 'POST':
        addr=ShippingAddress.objects.get(id=id)
        addr.name = request.POST.get("name")
        addr.lastname = request.POST.get("lastname")
        addr.email = request.POST.get("email")
        addr.phone = request.POST.get("phone")
        addr.street = request.POST.get("street")
        addr.apartment = request.POST.get("apartment")
        addr.city = request.POST.get("city")
        addr.state = request.POST.get("state")
        addr.zip = request.POST.get("zip")
        addr.save()
    orders = Order.objects.filter(complete=True)
    addresses = ShippingAddress.objects.filter(inactive=False).filter(user=customer)
    context = {
        'orders': orders,
        'addresses': addresses
    }
    return render(request,'user/profile.html', context)

def profileUpdate(request):
    email = request.user.email
    customer = myUser.objects.get(email=email)
    if request.method == 'POST':
        customer.first_name = request.POST.get("ltn__name")
        customer.last_name = request.POST.get("ltn__lastname")
        customer.username = request.POST.get("ltn__username")
        customer.email = request.POST.get("ltn__email")
        customer.save()
    orders = Order.objects.filter(complete=True)
    addresses = ShippingAddress.objects.filter(inactive=False).filter(user=customer)
    context = {
        'orders': orders,
        'addresses': addresses
    }
    return render(request,'user/profile.html', context)

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "user/reset-password/password_reset_email.html"
                    domain = request.get_host
                    c = {
				    "email":user.email,
					'domain': request.get_host,
					'site_name': 'Diagnog',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'https' or 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'saaltysugar@gmail.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("password_reset_done")
            else:
                messages.error(request, 'Email is not registered')
    password_reset_form = PasswordResetForm()
    return render(request, "user/reset-password/password_reset_form.html", context={"password_reset_form":password_reset_form})
