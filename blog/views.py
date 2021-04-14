from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Note
from .serializers import NoteSerializer


class AllNotesView(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request):
        notes = Note.objects.filter(public=True)
        serialized_notes = NoteSerializer(notes, many=True)

        return Response(serialized_notes.data, status=status.HTTP_200_OK)

    def post(self, request):
        serialized_notes = NoteSerializer(data=request.data)

        if serialized_notes.is_valid():
            serialized_notes.save(author=request.user)
            return Response(serialized_notes.data, status=status.HTTP_201_CREATED)

        return Response(serialized_notes.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleNoteView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, note_id):
        note = Note.objects.filter(pk=note_id).first()
        serialized_note = NoteSerializer(note)

        return Response(serialized_note.data)

    def patch(self, request, note_id):
        note = Note.objects.filter(pk=note_id, author=request.user).first()

        if not note:
            raise NotFound(f'Статья {note_id} у пользователя {request.user.username} не найдена')

        serialized_note = NoteSerializer(note, data=request.data, partial=True)

        if serialized_note.is_valid():
            serialized_note.save()
            return Response(serialized_note.data, status=status.HTTP_200_OK)

        return Response(serialized_note.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id):
        note = Note.objects.filter(pk=note_id, author=request.user).first()
        note.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


