from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'artists', views.ArtistViewSet)
router.register(r'albums', views.AlbumViewSet)
router.register(r'songs', views.SongViewSet)
router.register(r'album-songs', views.AlbumSongViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
