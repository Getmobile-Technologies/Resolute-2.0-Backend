# Generated by Django 4.2 on 2023-05-09 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisations',
            name='category',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
