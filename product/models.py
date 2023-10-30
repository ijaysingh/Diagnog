from datetime import datetime, timedelta
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from medical import settings
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.db.models import Count, Avg
from PIL import Image
from io import BytesIO

# Create your models here.

class category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category_name}"
    
    @property
    def get_products(self):
        return product.objects.filter(productCategory__category_name=self.category_name)

class product(models.Model):
    productName = models.CharField(max_length=50)
    productCategory = models.ManyToManyField(category)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    productImage = models.ImageField(blank=True, null=True)
    discount = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    pros = models.TextField(blank=True, null=True)
    cons = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    offer = models.BooleanField(default=False)
    class Meta:
        ordering = ['-date']



    def save(self, *args, **kwargs):    
        self.slug = slugify(self.productName)
        if self.productImage:
            im = Image.open(self.productImage)
            output = BytesIO()
            im = im.resize( (225,225) )
            im.save(output, format='JPEG', quality=90)
            output.seek(0)
            file_name = '{0}\{1}.jpg'.format(self.slug,"main")
            print(sys.getsizeof(output))
            self.productImage = InMemoryUploadedFile(output, 'ImageField',
                                          file_name,
                                          'image/jpeg', sys.getsizeof(output),
                                          None)
        super().save(*args, **kwargs)   
     

    def __str__(self):
        return f"{self.productName}" 

    @property
    def imgURL(self):
        try:
            url = self.productImage.url
        except:
            url = ''
        return url

    ## function to decide whether the product is new or not
    @property
    def isNew(self):
        try:
            # product registered date
            date = self.date.date()
            curr_date = datetime.now().date()

            # date after 30 days of product registered
            after_date = date + timedelta(days=30)

            if curr_date <= after_date:
                return True
            else:
                return False
        except:
            return False

    def averagereview(self):
        review = productReview.objects.filter(product=self).aggregate(avarage=Avg('rate'))
        avg=0
        if review["avarage"] is not None:
            avg=float(review["avarage"])
        return avg

    def countreview(self):
        reviews = productReview.objects.filter(product=self).aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt



class Images(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Image')

    def save(self, *args, **kwargs):
        if self.image:
            im = Image.open(self.image)
            output = BytesIO()
            im = im.resize( (300,300) )
            im.save(output, format='JPEG', quality=100)
            output.seek(0)
            file_name = '{0}\{1}.jpg'.format(self.product.slug,self.product.slug)
            self.image = InMemoryUploadedFile(output, 'ImageField',
                                          file_name,
                                          'image/jpeg', sys.getsizeof(output),
                                          None)
        super().save(*args, **kwargs)  

    def __str__(self):
        return self.product.slug

    @property
    def imgURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class productReview(models.Model):
    #user_id = models.ForeignKey(myUser, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    rate = models.IntegerField(default=1,null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    
    def __str__(self):
        return str(self.id)


class featuredPost(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='featuredPosts')

    def __str__(self):
        return self.product.productName


class trendingPost(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='trendingPost')

    def __str__(self):
        return self.product

class productInventory(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, null=True,blank=True)
    quantity = models.IntegerField()
    expiry_date = models.DateField(null=True, blank=True)