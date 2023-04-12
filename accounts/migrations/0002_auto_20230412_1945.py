# Generated by Django 4.2 on 2023-04-12 18:45
from django.db import migrations

def change_foreign_key_type(apps, schema_editor):
    schema_editor.execute('ALTER TABLE django_admin_log ALTER COLUMN user_id TYPE uuid USING user_id::uuid')

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(change_foreign_key_type),
    ]

