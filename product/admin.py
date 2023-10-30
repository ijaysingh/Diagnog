from django.contrib import admin
from .models import Images, product, category, featuredPost, productInventory, productReview, trendingPost
from django import forms
# Register your models here.

class productReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment', 'product', 'rate')

class ImageAdmin(admin.StackedInline):
    model = Images

@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]
    list_filter = ("productCategory", )


@admin.register(category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(productInventory)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ("product", ) 
    list_display = ['product', 'timestamp' ,'quantity', 'expiry_date']

@admin.register(Images)
class MultiImageAdmin(admin.ModelAdmin):
    pass




admin.site.register(featuredPost)
admin.site.register(trendingPost)
admin.site.register(productReview)
