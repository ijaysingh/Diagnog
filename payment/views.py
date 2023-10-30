from django.shortcuts import render, redirect
from order.models import Order, coupon
from django.contrib import messages
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

from user.models import ShippingAddress, myUser


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



def checkout(request):
	currency = 'INR'
	amount = 20000 # Rs. 200

	# Create a Razorpay Order
	razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

	# order id of newly created order.
	razorpay_order_id = razorpay_order['id']
	callback_url = 'paymenthandler/'

	# we need to pass these details to frontend.
	context = {}
	context['razorpay_order_id'] = razorpay_order_id
	context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
	context['currency'] = currency
	context['callback_url'] = callback_url
	if request.user.is_authenticated:
		email = request.user.email
		customer = myUser.objects.get(email=email)
		order = Order.objects.get(user=customer,complete = False)
		items = order.orderitem_set.all()
		addresses = ShippingAddress.objects.filter(user=customer)
		addrId = request.GET.get('addrId')
		context['razorpay_amount'] = order.get_cart_total
		if addrId:
			addr = ShippingAddress.objects.get(id=addrId)
			order.address = addr
			order.save()
		if request.method == 'POST' and is_ajax(request):
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
			order.address = newAddress
			order.save()
			addresses = ShippingAddress.objects.filter(user=customer)
			context['items'] = items
			context['order'] = order 
		context['addresses'] = addresses
	else:
		context['razorpay_amount'] = 0
	return render(request, 'payment/checkout.html', context=context)


def apply_coupon(request):
	code = request.GET.get('code')
	print(code)
	try:
		coupon_code = coupon.objects.get(code=code)
	except:
		messages.error(request,'Coupon Code is Invalid')
		return redirect(checkout)
	if request.user.is_authenticated:
		email = request.user.email
		customer = myUser.objects.get(email=email)
		order = Order.objects.get(user=customer,complete = False)
		order.coupon = coupon_code
		order.save()
	return redirect(checkout)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is None:
				amount = 20000 # Rs. 200
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputre of payment
					return render(request, 'payment/paymentsuccess.html')
				except:

					# if there is an error while capturing payment.
					return render(request, 'payment/paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'payment/paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()

