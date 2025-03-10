# Generated by Django 3.1.5 on 2024-05-03 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemuser',
            name='full_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='systemuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='systemuser',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='upload_thumbnail/'),
        ),
    ]
