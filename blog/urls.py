from django.contrib import admin
from django.urls import path, include

from .views import AllNotesView, SingleNoteView, AllCommentsView, SingleCommentView

app_name = 'blog'
urlpatterns = [
    path('note/', AllNotesView.as_view(), name='notes'),
    path('note/<int:note_id>', SingleNoteView.as_view(), name='single_note'),
    path('comment/', AllCommentsView.as_view(), name='notes'),
    path('comment/<int:comment_id>', SingleCommentView.as_view(), name='single_note'),
]