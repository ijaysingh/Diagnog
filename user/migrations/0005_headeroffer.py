# Generated by Django 4.0.4 on 2022-09-14 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_images'),
        ('user', '0004_shippingaddress_inactive'),
    ]

    operations = [
        migrations.CreateModel(
            name='headerOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='header/main.jpg')),
                ('main_line', models.CharField(max_length=50)),
                ('offer_line', models.CharField(max_length=50)),
                ('starting_at', models.CharField(max_length=50)),
                ('product_list', models.ManyToManyField(to='product.product')),
            ],
        ),
    ]
