# Generated by Django 2.1.15 on 2023-09-13 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_user_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='username',
        ),
    ]