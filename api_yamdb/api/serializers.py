from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Categorie, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categorie
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('__all__')
        model = Title


class TitleSerializerCreate(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categorie.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = ('__all__')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = '__all__'
        read_only_fields = ['title']
        model = Review

    def validate(self, data):
        request = self.context.get('request')
        if request.method == 'PATCH':
            return data

        title_id = request.parser_context.get('kwargs').get('title_id')
        title = get_object_or_404(Title, id=title_id)
        user = self.context['request'].user
        if Review.objects.filter(title=title, author=user).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        many=False,
        slug_field='username',
        read_only=True)

    class Meta:
        fields = '__all__'
        read_only_fields = ['review']
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'role',
                  'email',
                  'first_name',
                  'last_name',
                  'bio')


class UserRegistrSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'email']
        model = User

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'имя Ме запрещено')
        return data


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['email']
        model = User
        extra_kwargs = {
            'email': {'required': True}
        }
