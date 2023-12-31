# Generated by Django 4.0.4 on 2022-09-05 17:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_productinventory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreview',
            name='rating',
        ),
        migrations.AddField(
            model_name='productreview',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productreview',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='productreview',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='productreview',
            name='rate',
            field=models.IntegerField(default=1),
        ),
    ]
