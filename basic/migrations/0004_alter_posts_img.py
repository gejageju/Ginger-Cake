# Generated by Django 4.0.1 on 2022-12-24 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0003_posts_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='img',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]