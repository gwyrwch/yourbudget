# Generated by Django 2.2 on 2019-05-11 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipt_back', '0002_user_telegram_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fav_product',
            field=models.CharField(default='ice-cream', max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=6),
        ),
    ]
