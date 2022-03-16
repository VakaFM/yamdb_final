from django.contrib import admin

from .models import Categorie, Comment, Genre, Review, Title, User

admin.site.register(User)
admin.site.register(Title)
admin.site.register(Categorie)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Genre)
