# Generated by Django 4.2 on 2023-05-17 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_category_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
