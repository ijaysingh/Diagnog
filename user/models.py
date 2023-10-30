from django.db import models
from django.contrib.auth.models import AbstractUser
from medical import settings
from product.models import product

# Create your models here.

state_choices = (
    ("Andhra Pradesh","Andhra Pradesh"),
    ("Arunachal Pradesh ","Arunachal Pradesh "),
    ("Assam","Assam"),
    ("Bihar","Bihar"),
    ("Chhattisgarh","Chhattisgarh"),
    ("Goa","Goa"),
    ("Gujarat","Gujarat"),
    ("Haryana","Haryana"),
    ("Himachal Pradesh","Himachal Pradesh"),
    ("Jammu and Kashmir ","Jammu and Kashmir "),
    ("Jharkhand","Jharkhand"),
    ("Karnataka","Karnataka"),
    ("Kerala","Kerala"),
    ("Madhya Pradesh","Madhya Pradesh"),
    ("Maharashtra","Maharashtra"),
    ("Manipur","Manipur"),
    ("Meghalaya","Meghalaya"),
    ("Mizoram","Mizoram"),
    ("Nagaland","Nagaland"),
    ("Odisha","Odisha"),
    ("Punjab","Punjab"),
    ("Rajasthan","Rajasthan"),
    ("Sikkim","Sikkim"),
    ("Tamil Nadu","Tamil Nadu"),
    ("Telangana","Telangana"),
    ("Tripura","Tripura"),
    ("Uttar Pradesh","Uttar Pradesh"),
    ("Uttarakhand","Uttarakhand"),
    ("West Bengal","West Bengal"),
    ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
    ("Chandigarh","Chandigarh"),
    ("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
    ("Daman and Diu","Daman and Diu"),
    ("Lakshadweep","Lakshadweep"),
    ("National Capital Territory of Delhi","National Capital Territory of Delhi"),
    ("Puducherry","Puducherry")
)


class wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class myUser(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField('email address', unique=True)
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.IntegerField()
    street_address = models.TextField()
    apartment_address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(choices=state_choices,max_length=255, null=True, blank=True)
    zip = models.IntegerField()
    selected = models.BooleanField(default=False)
    inactive = models.BooleanField(default=False)
    def __str__(self):
        return self.first_name + " " + self.last_name

class headerOffer(models.Model):
    image = models.ImageField(upload_to='header/', null=True, blank=True)
    image_1 = models.ImageField(upload_to='header/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='header/', null=True, blank=True)
    main_line = models.CharField(max_length=150)
    offer_line = models.CharField(max_length=150)
    starting_at = models.CharField(max_length=50)
    product_list = models.ManyToManyField(product)
    enable = models.BooleanField(default=False)

    @property
    def imgURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.product_list:
    #         for i in self.product_list.all():
    #             i.offer=True
    #             i.save()
    #     try:
    #         if self.enable == True:
    #             sliders = headerOffer.objects.filter(enable=True)
    #             for slider in sliders:
    #                 slider.enable=False
    #                 slider.save()
    #                 for item in slider.product_list.all():
    #                     item.offer = False
    #                     item.save()
    #         if self.product_list:
    #             for i in self.product_list.all():
    #                 i.offer=True
    #                 i.save()
    #         super().save(*args, **kwargs)
    #     except:
    #         super().save(*args, **kwargs)