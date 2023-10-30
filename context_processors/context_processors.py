import json
# from statistics import quantiles
from order.models import Order
from product.models import product, category
from user.models import myUser, wishlist

# For _footer.html template file
def products_context_processor(request):
    categories = category.objects.all()
    products = product.objects.all()
    if request.user.is_authenticated:
        email = request.user.email
        customer = myUser.objects.get(email=email)
        order, created = Order.objects.get_or_create(user=customer,complete = False)
        items = order.orderitem_set.all()
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = json.loads("{}")
        items = []
        order = {'get_cart_total':0,'get_cart_total_item':0}
        
        for i in cart:
            productitem = product.objects.get(id=i)
            quantity = int(cart[i]['quantity'])
            total = (productitem.discount_price * quantity)
            items.append({'product': productitem, 'get_final_price': total, 'quantity': quantity})
            order['get_cart_total'] += total
            order['get_cart_total_item'] += quantity
    return {'categories': categories, 'products': products, 'order': order, 'items': items}
