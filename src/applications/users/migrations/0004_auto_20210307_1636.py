# Generated by Django 3.1.7 on 2021-03-07 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_is_staff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='user_name',
            new_name='username',
        ),
    ]