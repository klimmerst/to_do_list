from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import ListField, ChoiceField, BooleanField
from rest_framework.serializers import Serializer

from .models import Note, Comment


class AuthorSerializer(serializers.ModelSerializer):
    """Полная информация по автору"""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined', )
        # readonly_field = ('', )


class AuthorMiniSerializer(serializers.ModelSerializer):
    """Краткая информация по автору"""

    class Meta:
        model = User
        fields = ('id', 'username', )


class NoteMiniSerializer(serializers.ModelSerializer):
    """Краткая информация по заметке"""

    note_id = serializers.IntegerField(source='id')

    class Meta:
        model = Note
        fields = ('note_id', 'author_id', )


class CommentMiniSerializer(serializers.ModelSerializer):
    """Краткая информацию по комментарию"""

    comment_id = serializers.IntegerField(source='id')

    class Meta:
        model = Comment
        fields = ('comment_id', 'author_id', )


class CommentSerializer(serializers.ModelSerializer):
    """Полная информация по одному комментарию и краткая по заметке"""

    author = AuthorSerializer(read_only=True)
    note = NoteMiniSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('author', 'message', 'date_add', 'note', )


class AllCommentsSerializer(serializers.ModelSerializer):
    """Полная информация по всем комментариям и краткая по заметкам"""

    note = NoteMiniSerializer(read_only=True)
    comment_id = serializers.IntegerField(source='id')
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('comment_id', 'author_id', 'author', 'message', 'date_add', 'note', )


class AllNotesSerializer(serializers.ModelSerializer):
    """Полная информация по всем заметкам и краткая по комментариям"""

    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    comments = CommentMiniSerializer(many=True, read_only=True)

    state = serializers.SerializerMethodField('get_state')

    def get_state(self, obj):
        return obj.get_state_display()

    note_id = serializers.IntegerField(source='id')

    class Meta:
        model = Note
        fields = ('note_id', 'author_id', 'author', 'title', 'date_add', 'importance', 'state', 'public', 'comments')


class SingleNoteSerializer(serializers.ModelSerializer):
    """Полная информация по одной заметке и по каждому её комментарию"""

    author = AuthorSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    state = serializers.SerializerMethodField('get_state')

    def get_state(self, obj):
        return obj.get_state_display()

    class Meta:
        model = Note
        fields = ('author', 'title', 'text', 'date_add', 'importance', 'state', 'public', 'comments', )
        read_only_field = ('author', )


class QuerySerializer(Serializer):
    state = ListField(child=ChoiceField(choices=Note.STATE), required=False)
    importance = BooleanField()
    public = BooleanField()