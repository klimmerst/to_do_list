from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Note
from blog.serializers import NoteSerializer


class NoteView(APIView):

    def get(self, request):
        notes = Note.objects.all()
        serialized_notes = NoteSerializer(notes, many=True)

        return Response(serialized_notes.data, status=status.HTTP_200_OK)

    def post(self, request):
        serialized_notes = NoteSerializer(data=request.data)

        if serialized_notes.is_valid():
            serialized_notes.save(author=request.user)
            return Response(serialized_notes.data, status=status.HTTP_201_CREATED)

        return Response(serialized_notes.errors, status=status.HTTP_400_BAD_REQUEST)


