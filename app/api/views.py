from rest_framework import viewsets
from songs.models import Artist, Album, Song, AlbumSong
from .serializers import (
    ArtistSerializer,
    AlbumSerializer,
    SongSerializer,
    AlbumSongCreateSerializer,
)


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all().prefetch_related("albums__songs")
    serializer_class = ArtistSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all().prefetch_related("songs")
    serializer_class = AlbumSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class AlbumSongViewSet(viewsets.ModelViewSet):
    queryset = AlbumSong.objects.all()
    serializer_class = AlbumSongCreateSerializer
