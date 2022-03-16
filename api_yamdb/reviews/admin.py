from django.contrib import admin

from .models import User, Title, Categorie, Review, Comment, Genre


admin.site.register(User)
admin.site.register(Title)
admin.site.register(Categorie)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Genre)
