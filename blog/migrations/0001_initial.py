# Generated by Django 2.0.3 on 2018-04-27 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(help_text='Enter a brief description of the blog', max_length=2000)),
                ('date', models.DateField()),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Blogger',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bio', models.TextField(help_text='Enter something about your bio', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.TextField(help_text='Enter your comment for the blog', max_length=3000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blogger')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blogger'),
        ),
    ]
