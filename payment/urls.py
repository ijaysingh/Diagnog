
from django.urls import path
from payment import views

urlpatterns = [
	path('checkout/', views.checkout, name='checkout'),
    path('checkout/apply_coupon', views.apply_coupon, name='apply_coupon'),
	path('checkout/paymenthandler/', views.paymenthandler, name='paymenthandler'),
]
