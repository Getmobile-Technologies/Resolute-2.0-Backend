# Generated by Django 4.2 on 2023-04-25 23:45

import accounts.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=250, verbose_name='first_name')),
                ('last_name', models.CharField(max_length=250, verbose_name='last_name')),
                ('phone', models.CharField(max_length=200, null=True, unique=True, verbose_name='phone')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='email')),
                ('role', models.CharField(max_length=100, null=True, verbose_name='role')),
                ('password', models.CharField(max_length=100, null=True, verbose_name='password')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('is_admin', models.BooleanField(default=False, verbose_name='admin')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', accounts.managers.UserManager()),
            ],
        ),
    ]
