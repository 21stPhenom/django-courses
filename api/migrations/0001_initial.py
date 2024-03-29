# Generated by Django 5.0 on 2024-01-03 15:10

import autoslug.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Course Title')),
                ('price', models.FloatField(default=1.0, verbose_name='Course Price')),
                ('duration', models.PositiveIntegerField(default=1, verbose_name='Course Duration')),
                ('currency', models.CharField(default='NGN', max_length=3, verbose_name='Course Currency')),
                ('slug_title', autoslug.fields.AutoSlugField(editable=False, max_length=200, populate_from='title', unique=True, verbose_name='Course Slug')),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_updated', '-date_uploaded'],
                'get_latest_by': ['-date_updated', '-date_uploaded'],
            },
        ),
    ]
