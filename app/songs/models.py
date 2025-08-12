from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название исполнителя")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"


class Album(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название альбома")
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="albums",
        verbose_name="Исполнитель",
    )
    release_year = models.PositiveIntegerField(verbose_name="Год выпуска")

    def __str__(self):
        return f"{self.title} ({self.artist.name}, {self.release_year})"

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"


class Song(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название песни")
    albums = models.ManyToManyField(
        Album, through="AlbumSong", related_name="songs", verbose_name="Альбомы"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Песня"
        verbose_name_plural = "Песни"


class AlbumSong(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name="Альбом")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, verbose_name="Песня")
    track_number = models.PositiveIntegerField(
        verbose_name="Порядковый номер в альбоме"
    )

    def __str__(self):
        return f"{self.track_number}. {self.song.title} ({self.album.title})"

    class Meta:
        verbose_name = "Песня в альбоме"
        verbose_name_plural = "Песни в альбомах"
        unique_together = [["album", "track_number"], ["album", "song"]]
        ordering = ["album", "track_number"]
