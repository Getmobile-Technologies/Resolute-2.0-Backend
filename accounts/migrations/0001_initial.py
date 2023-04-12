# Generated by Django 4.2 on 2023-04-12 14:15

import accounts.managers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('full_name', models.CharField(max_length=250, verbose_name='name')),
                ('phone', models.IntegerField(unique=True, verbose_name='phone')),
                ('location', models.CharField(max_length=200, null=True, verbose_name='location')),
                ('role', models.CharField(max_length=100, null=True, verbose_name='role')),
                ('password', models.CharField(max_length=100, null=True, verbose_name='password')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('is_admin', models.BooleanField(default=False, verbose_name='admin')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser')),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mapped_users', to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', accounts.managers.UserManager()),
            ],
        ),
        migrations.RunSQL('ALTER TABLE accounts_user ALTER COLUMN id TYPE uuid USING id::uuid;'),
    ]

