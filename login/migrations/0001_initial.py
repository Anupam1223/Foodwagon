# Generated by Django 3.2.5 on 2021-07-14 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(default='a@gmail.com', max_length=255, unique=True)),
                ('address', models.TextField(blank=True, max_length=30)),
                ('first_name', models.TextField(blank=True, default='eg aster', max_length=30)),
                ('last_name', models.TextField(blank=True, max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('admin', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
