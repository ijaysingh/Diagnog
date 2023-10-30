from django.urls import path, include
from . import views

urlpatterns = [
    path('cart/', views.cartPage, name="cart"),
    path('cart/update/',views.update_cart, name="update"),
    path('track-order/', views.trackOrder, name="order_tracking"),
    # path('checkout/', views.checkout, name="checkout"),
]