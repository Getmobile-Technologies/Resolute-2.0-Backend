# Generated by Django 4.2 on 2023-05-09 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='callrequest',
            name='organisation',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='images',
            name='organisation',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='notifications',
            name='organisation',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='panicrequest',
            name='organisation',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='stafflocation',
            name='organisation',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='trackmerequest',
            name='organisation',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
