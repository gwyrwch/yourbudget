# Generated by Django 2.2 on 2019-05-06 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipt_back', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_username',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
