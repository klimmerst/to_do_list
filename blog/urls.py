from django.contrib import admin
from django.urls import path, include

from .views import AllNotesView, SingleNoteView

app_name = 'blog'
urlpatterns = [
    path('note/', AllNotesView.as_view(), name='notes'),
    path('note/<int:note_id>', SingleNoteView.as_view(), name='single_note'),
]