# Generated by Django 2.0.3 on 2018-04-28 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180428_1359'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['date']},
        ),
    ]
