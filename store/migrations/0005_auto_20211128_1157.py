# Generated by Django 2.2.20 on 2021-11-28 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20211127_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Description',
            field=models.CharField(default='bez popisu', max_length=500),
        ),
    ]
