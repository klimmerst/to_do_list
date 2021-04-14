from django.contrib.auth.models import User
from rest_framework import serializers

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

    note_id = serializers.SerializerMethodField('get_note_id')
    def get_note_id(self, obj):
        return obj.pk

    # Закомментировал код ниже, потому что он больле не нужен: вспомнил, что author_id и так есть в БД,
    # также понял, что username можно достать через obj.author.username. Но таки интересно почему f-строка
    # так себя ведёт -- на f'obj.author' выдаёт username, а без f'' DEBUG выдаёт:
    # "Object of type User is not JSON serializable"

    # author_id = serializers.SerializerMethodField('get_author_id')
    # def get_author_id(self, obj):
    #     return obj.author_id  # Если тут прописать f'{obj.author}', то он выдаст "klimmerst2" - не понимаю
                                # почему, ведь obj это экземпляр Note, значит надо смотреть
                                # в blog_note, а там нет такого поля как author.

    class Meta:
        model = Note
        fields = ('note_id', 'author_id', )


class CommentMiniSerializer(serializers.ModelSerializer):
    """Краткая информацию по комментарию"""

    comment_id = serializers.SerializerMethodField('get_comment_id')

    def get_comment_id(self, obj):
        return obj.pk

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

    comment_id = serializers.SerializerMethodField('get_comment_id')

    def get_comment_id(self, obj):
        return obj.pk

    author = serializers.SerializerMethodField('get_username')

    def get_username(self, obj):
        return obj.author.username

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

    note_id = serializers.SerializerMethodField('get_note_id')

    def get_note_id(self, obj):
        return obj.pk

    class Meta:
        model = Note
        fields = ('note_id', 'author_id', 'author', 'title', 'date_add', 'importance', 'state', 'public', 'comments')
        # read_only_field = ( )


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