from django.db import models
from medical import settings
from product.models import product
from user.models import ShippingAddress

# Create your models here.
class coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    valid_date = models.DateField(null=True, blank=True)
    min_value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.code

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    complete = models.BooleanField(default=False,null=True, blank=True)
    date_ordered = models.DateField(auto_now_add=True)
    address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    coupon = models.ForeignKey(coupon,on_delete=models.SET_NULL,null=True, blank=True)
    def __str__(self):
        return self.user.username

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_final_price for item in orderitems])
        return total

    def get_cart_total_after_coupon(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_final_price for item in orderitems])
        if self.coupon:
            total = total - self.coupon.amount
        return total

    @property
    def get_cart_final(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_final_price for item in orderitems])
        return total
    
    @property
    def get_cart_total_item(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product}"

    @property
    def get_total_item_price(self):
        return self.quantity * self.product.price

    @property
    def get_total_discount_item_price(self):
        return self.quantity * self.product.discount_price

    @property
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    @property
    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_item_price
        return self.get_total_item_price()




