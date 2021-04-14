from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Note


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')


class NoteSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    state = serializers.SerializerMethodField('get_state')

    def get_state(self, obj):
        return obj.get_state_display()

    class Meta:
        model = Note
        fields = ('author', 'title', 'date_add', 'importance', 'state', 'public')
        read_only_field = ('author', )