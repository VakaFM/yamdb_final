from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    RegistrUserView, ReviewViewSet, TitleViewSet, UserViewSet)

router_v1 = SimpleRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
router_v1.register('titles', TitleViewSet, basename='Title')
router_v1.register('categories', CategoryViewSet, basename='Category')
router_v1.register('genres', GenreViewSet, basename='Genre')


urlpatterns = [
    path('v1/auth/signup/', RegistrUserView.as_view(), name='registr'),
    path('v1/auth/token/', views.get_token, name='get_token'),
    path('v1/', include(router_v1.urls)),
]
