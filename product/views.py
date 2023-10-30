import email
import math
from unicodedata import category, name
from django.db.models import Q
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from order.models import Order, OrderItem
from django.core.paginator import Paginator
from product.models import  Images, product, productReview
from user.models import myUser, wishlist
from django.template.defaulttags import register
from product.templatetags import extras

# Create your views here.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def getReviewAverage(reviews):
    avg = 0
    count = 0
    for review in reviews:
        avg += review.rate
        count += 1 
    avg = avg / count
    avg = round(avg,1)
    n = avg - math.floor(avg)
    avg = math.floor(avg)
    isHalf = False
    if(n>0.3):
        isHalf = True
    elif(n>0.8):
        isHalf = False
        avg+=1
    return avg, isHalf


def productDetails(request, slug):
    context = {}
    try:
        item = product.objects.get(slug=slug)
    except:
        return redirect('error')
    images = Images.objects.filter(product=item)
    review = productReview.objects.filter(product = item)
    categories = item.productCategory.all()
    rel_product = set()
    for category in categories:
        for relProduct in category.get_products:
            rel_product.add(relProduct)
    if review:
        reviewAvg, isHalf = getReviewAverage(review)
    else:
        reviewAvg, isHalf = None, None
    if is_ajax(request=request):
        ID = request.GET.get('id')
        addWishlist = request.GET.get('wishlist')
        addCart = request.GET.get('cart')
        quantity = request.GET.get('quantity')
        clickedProduct = product.objects.get(id=ID)
        if request.user.is_authenticated:
            email = request.user.email
            print(email)
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
    context['product'] =  item
    context['reviews'] = review
    context['images'] = images
    context['reviewAvg'] = reviewAvg
    context['isHalf'] = isHalf
    context['rel_product'] = rel_product
    return render(request, 'product/product_details.html', context)

@register.filter
def get_range(value):
    return range(1,value+1)

def productSearch(request):
    context = {}
    filter_by = request.GET.get('filter', "")
    order_by = request.GET.get("orderby", "id").strip()
    print(order_by)
    if filter_by != "":
        products = product.objects.filter(Q(productName__contains=filter_by) | Q(description__contains=filter_by) | Q(productCategory__category_name__contains=filter_by)).order_by(order_by).distinct()
    else:
        products = product.objects.all().order_by(order_by).distinct()
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
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
    context['products'] = page_obj
    context['filter_by'] = filter_by
    context['order_by'] = order_by
    return render(request, 'product/product_search.html', context)


def product_review(request):
    product_id = request.GET.get('product_id')
    productName = product.objects.get(id=product_id)
    comment = request.GET.get('comment')
    rate = request.GET.get('rate')
    if request.user.is_authenticated:
        name = request.user
        email = request.user.email
    else:
        name = request.GET.get('comment_name')
        email = request.GET.get('comment_email')
    productReview(product=productName, comment=comment, rate=rate, name=name, email=email).save()
    
    return redirect('product_details', slug=productName.slug,)



def temp(request):
    return render(request, 'temp.html',)