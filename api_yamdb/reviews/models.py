import datetime

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class MyUserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("Вы не ввели Email")
        if not username:
            raise ValueError("Вы не ввели Логин")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password, **extra_fields):
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        return self._create_user(email, username, password,
                                 is_staff=True, is_superuser=True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default='user',
        verbose_name='user role')
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        verbose_name='username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    first_name = models.CharField(verbose_name='first name',
                                  max_length=150,
                                  blank=True)
    last_name = models.CharField(verbose_name='last name',
                                 max_length=150,
                                 blank=True)
    is_staff = models.BooleanField(
        verbose_name='staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    bio = models.TextField(verbose_name='biography',
                           blank=True)
    email = models.EmailField(verbose_name='email address',
                              unique=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = MyUserManager()

    def __str__(self):
        return '%s (%s)' % (self.get_full_name(), self.email)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'


class Categorie(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    name = models.CharField(max_length=100, verbose_name='name')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='name genre')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(datetime.date.today().year), ],
        verbose_name='year')
    description = models.CharField(max_length=300,
                                   blank=True,
                                   null=True,
                                   verbose_name='description')
    genre = models.ManyToManyField(Genre, verbose_name='genre')
    category = models.ForeignKey(Categorie,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='category')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение')
    score = models.PositiveSmallIntegerField(
        default=None,
        null=True,
        blank=True,
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        verbose_name='Оценка')
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата ревью',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='UniqueReviewEntry'),
        ]

    def __str__(self):
        return f'Отзыв на {self.title}, автор: {self.author}'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор')
    text = models.TextField('Текст')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв')
    pub_date = models.DateTimeField('Дата ревью', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий на {self.review}, автор: {self.author}'


class ConfirmCodes(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='ConfirmCodes',
        verbose_name='owner of code')
    reg_code = models.CharField(max_length=6,
                                default=None,
                                null=True,
                                blank=True,
                                verbose_name='registratoin code')
    code_date = models.DateTimeField('Дата создания кода', auto_now_add=True)
