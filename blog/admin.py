from django.contrib import admin
from django.forms import models

from blog.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    fields = ('id','title', 'text', 'date_add', 'importance', )
    list_display = ('title', 'text', 'date_add', 'importance', )
    readonly_fields = ('date_add', )
    list_filter = ('date_add', 'importance', )

from django.contrib import admin

# Register your models here.
