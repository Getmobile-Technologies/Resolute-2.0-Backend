# Generated by Django 4.2 on 2023-05-19 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_emergencycontact_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='emergencycontact',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
