
from django.urls import path, include
from . import views

urlpatterns = [
    path('product-details/<slug:slug>/', views.productDetails, name="product_details"),
    path('product/', views.productSearch, name="product_search"),
    path('product/addreview', views.product_review, name="product_review"),
]