from django.contrib import admin

from order.models import Order, OrderItem, coupon

# Register your models here.

@admin.register(Order)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderItem)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(coupon)
class CouponAdmin(admin.ModelAdmin):
    pass