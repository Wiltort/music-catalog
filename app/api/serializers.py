from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from songs.models import Artist, Album, Song, AlbumSong


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["id", "title"]


class AlbumSongSerializer(serializers.ModelSerializer):
    song = SongSerializer()
    song_id = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all(), source="song", write_only=True
    )

    class Meta:
        model = AlbumSong
        fields = ["song", "song_id", "track_number"]

    def validate(self, data):
        album = self.context.get("album")
        track_number = data.get("track_number")

        if album and track_number:
            if AlbumSong.objects.filter(
                album=album, track_number=track_number
            ).exists():
                raise ValidationError(
                    f"Трек номер {track_number} уже существует в этом альбоме"
                )

        return data


class AlbumSerializer(serializers.ModelSerializer):
    songs = AlbumSongSerializer(source="albumsong_set", many=True, required=False)

    class Meta:
        model = Album
        fields = ["id", "title", "artist", "release_year", "songs"]

    def validate(self, data):
        songs_data = data.get('albumsong_set', [])
        
        if songs_data:
            track_numbers = [song['track_number'] for song in songs_data]
            if len(track_numbers) != len(set(track_numbers)):
                raise ValidationError(
                    "В одном альбоме не может быть двух песен с одинаковым порядковым номером"
                )
        
        return data

    def create(self, validated_data):
        songs_data = validated_data.pop("albumsong_set", [])

        album = Album.objects.create(**validated_data)
        # Внимание! Так создавать можно только новые песни!
        for song_data in songs_data:
            song = Song.objects.create(title=song_data["song"]["title"])
            AlbumSong.objects.create(
                album=album,
                song=song,
                track_number=song_data["track_number"],
            )

        return album

    def update(self, instance, validated_data):
        songs_data = validated_data.pop("albumsong_set", None)

        instance.title = validated_data.get("title", instance.title)
        instance.artist = validated_data.get("artist", instance.artist)
        instance.release_year = validated_data.get(
            "release_year", instance.release_year
        )
        instance.save()

        if songs_data is not None:
            instance.albumsong_set.all().delete()

            for song_data in songs_data:
                # Внимание! Так создаются новые песни!
                song = Song.objects.create(title=song_data["song"]["title"])
                AlbumSong.objects.create(
                    album=instance,
                    song=song,
                    track_number=song_data["track_number"],
                )

        return instance


class ArtistSerializer(serializers.ModelSerializer):
    albums = AlbumSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = ["id", "name", "albums"]


class AlbumSongCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumSong
        fields = ["album", "song", "track_number"]
