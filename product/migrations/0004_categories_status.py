# Generated by Django 3.2.5 on 2021-07-26 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210726_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
