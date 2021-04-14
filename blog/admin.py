from django.contrib import admin
from django.forms import models

from blog.models import Note, Comment


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'text', 'date_add', 'importance', 'public', 'state', )
    fields = (('title', 'state', ), 'text', ('importance', 'public', ), )
    readonly_fields = ('date_add', )
    list_filter = ('importance', 'state', 'public', )

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, "author") or not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'message', 'date_add', 'note', )
    fields = ('message', 'note', )
    readonly_fields = ('date_add', )

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, "author") or not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)