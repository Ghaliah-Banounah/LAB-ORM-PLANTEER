# Generated by Django 5.1.3 on 2024-11-18 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0003_comments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]
