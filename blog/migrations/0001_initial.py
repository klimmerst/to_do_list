# Generated by Django 3.2 on 2021-04-11 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('text', models.TextField(default='', verbose_name='Текст заметки')),
                ('date_add', models.TimeField(auto_now=True, verbose_name='Время последней редакции')),
                ('importance', models.BooleanField(default=False, verbose_name='Важность заметки')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='authors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
