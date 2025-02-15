# Generated by Django 3.2.5 on 2021-08-03 08:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_alter_order_date_of_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_of_order',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='order',
            name='day',
            field=models.DateTimeField(max_length=100),
        ),
    ]
