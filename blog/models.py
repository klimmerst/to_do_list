from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    STATE = (
        (0, "Активно"),
        (1, "Отложено"),
        (2, "Выполнено"),
    )

    author = models.ForeignKey(User, related_name='authors_note', on_delete=models.PROTECT)
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    text = models.TextField(default='', verbose_name='Текст заметки')
    date_add = models.TimeField(default=datetime.now() + timedelta(days=1), verbose_name="Дата создания")
    importance = models.BooleanField(default=False, verbose_name='Важная')
    public = models.BooleanField(default=False, verbose_name='Публичная')
    state = models.IntegerField(default=0, choices=STATE, verbose_name='Статус состояния')

    def __str__(self):
        return f'{self.title}: {self.get_state_display()}'


class Comment(models.Model):

    author = models.ForeignKey(User, related_name='authors_comment', on_delete=models.CASCADE)
    note = models.ForeignKey(Note, related_name='comments', on_delete=models.CASCADE)
    message = models.TextField(default='', verbose_name='Комментарий заметки')
    date_add = models.TimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f'{self.message}'