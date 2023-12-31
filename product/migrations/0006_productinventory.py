# Generated by Django 4.0.4 on 2022-09-03 17:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_product_options_product_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='productInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('quantity', models.IntegerField()),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
