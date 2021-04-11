from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    text = models.TextField(default='', verbose_name='Текст заметки')
    author = models.ForeignKey(User, related_name='authors', on_delete=models.PROTECT)
    date_add = models.TimeField(auto_now=True, verbose_name="Время последней редакции")
    importance = models.BooleanField(default=False, verbose_name='Важность заметки')
    # privacy = models.
    # state = models.