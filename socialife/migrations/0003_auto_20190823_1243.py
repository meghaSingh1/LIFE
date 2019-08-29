# Generated by Django 2.2.4 on 2019-08-23 05:43

from django.db import migrations, models
import socialife.models


class Migration(migrations.Migration):

    dependencies = [
        ('socialife', '0002_myuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=socialife.models.MyUser.user_directory_path),
        ),
    ]