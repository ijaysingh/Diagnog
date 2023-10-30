from django.contrib import admin

from user.models import ShippingAddress, headerOffer, myUser, wishlist

# Register your models here.
@admin.register(myUser)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(wishlist)
class wishlistAdmin(admin.ModelAdmin):
    pass

def delete_model(modeladmin, request, queryset):
    for obj in queryset:
        for item in obj.product_list.all():
            item.offer = False
            item.save()
        obj.delete()

@admin.register(headerOffer)
class headerAdmin(admin.ModelAdmin):
    list_display = ["offer_line","enable"]
    actions = [delete_model]

@admin.register(ShippingAddress)
class adressAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name']
    list_filter = ('user', )