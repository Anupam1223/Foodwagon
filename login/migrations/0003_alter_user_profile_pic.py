# Generated by Django 3.2.5 on 2021-07-28 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_vendorinfo_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='images/user/'),
        ),
    ]
