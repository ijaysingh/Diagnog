# Generated by Django 4.0.4 on 2022-09-06 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_remove_productreview_rating_productreview_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='rate',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
