# Generated by Django 3.2.5 on 2021-07-28 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorinfo',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='images/banner/'),
        ),
    ]
