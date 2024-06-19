# Generated by Django 3.1.5 on 2024-05-02 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('complaint', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='answer_images/')),
                ('video', models.FileField(blank=True, null=True, upload_to='answer_videos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('complaint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='complaint.complaint')),
                ('respondent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers_given', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
