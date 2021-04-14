from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Note, Comment
from .serializers import AllNotesSerializer, CommentSerializer, SingleNoteSerializer, AllCommentsSerializer


class AllNotesView(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request):
        notes = Note.objects.filter(public=True)
        serialized_notes = AllNotesSerializer(notes, many=True)

        return Response(serialized_notes.data, status=status.HTTP_200_OK)

    def post(self, request):
        serialized_notes = AllNotesSerializer(data=request.data)

        if serialized_notes.is_valid():
            serialized_notes.save(author=request.user)
            return Response(serialized_notes.data, status=status.HTTP_201_CREATED)

        return Response(serialized_notes.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleNoteView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, note_id):
        note = Note.objects.filter(pk=note_id).first()
        serialized_note = SingleNoteSerializer(note)

        return Response(serialized_note.data)

    def patch(self, request, note_id):
        note = Note.objects.filter(pk=note_id, author=request.user).first()

        if not note:
            raise NotFound(f'Статья {note_id} у пользователя {request.user.username} не найдена')

        serialized_note = SingleNoteSerializer(note, data=request.data, partial=True)

        if serialized_note.is_valid():
            serialized_note.save()
            return Response(serialized_note.data, status=status.HTTP_200_OK)

        return Response(serialized_note.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id):
        note = Note.objects.filter(pk=note_id, author=request.user).first()
        note.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AllCommentsView(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request):
        notes = Comment.objects.all()
        serialized_notes = AllCommentsSerializer(notes, many=True)

        return Response(serialized_notes.data, status=status.HTTP_200_OK)

    def post(self, request):
        serialized_notes = AllCommentsSerializer(data=request.data)

        if serialized_notes.is_valid():
            serialized_notes.save(author=request.user)
            return Response(serialized_notes.data, status=status.HTTP_201_CREATED)

        return Response(serialized_notes.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleCommentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, comment_id):
        note = Comment.objects.filter(pk=comment_id).first()
        serialized_note = CommentSerializer(note)

        return Response(serialized_note.data)

    def patch(self, request, comment_id):
        note = Comment.objects.filter(pk=comment_id, author=request.user).first()

        if not note:
            raise NotFound(f'Комментарий {comment_id} у пользователя {request.user.username} не найден')

        serialized_note = CommentSerializer(note, data=request.data, partial=True)

        if serialized_note.is_valid():
            serialized_note.save()
            return Response(serialized_note.data, status=status.HTTP_200_OK)

        return Response(serialized_note.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        note = Comment.objects.filter(pk=comment_id, author=request.user).first()
        note.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



