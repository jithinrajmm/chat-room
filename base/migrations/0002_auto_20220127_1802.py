# Generated by Django 3.2.4 on 2022-01-27 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(default='avatar.svg', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]
