# Generated by Django 4.2 on 2023-04-27 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(max_length=300, null=True, verbose_name='location'),
        ),
    ]
