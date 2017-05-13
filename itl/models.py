from django.db import models


class Artist(models.Model):
    name = models.CharField(default="Artist Unknown", max_length=255)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(default="Album Unknown", max_length=255)
    artist = models.ForeignKey(Artist, null=True, blank=True, on_delete=models.SET_NULL)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    album_rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Kind(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Playlist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Track(models.Model):
    persistent_id = models.CharField(max_length=255, blank=True)
    title = models.CharField(default="Unknown", max_length=255)
    artist = models.ForeignKey(Artist, blank=True, null=True)
    composer = models.ForeignKey(Artist, blank=True, null=True, related_name="track_composer")
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    album = models.ForeignKey(Album, blank=True, null=True)
    genre = models.ForeignKey(Genre, blank=True, null=True)
    kind = models.ForeignKey(Kind, blank=True, null=True)
    loved = models.BooleanField(default=False)
    compilation = models.BooleanField(default=False)
    size = models.IntegerField(null=True, blank=True)
    bit_rate = models.IntegerField(null=True, blank=True)
    total_time = models.IntegerField(null=True, blank=True)
    track_number = models.IntegerField(null=True, blank=True)
    track_count = models.IntegerField(null=True, blank=True)
    sample_rate = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    play_count = models.IntegerField(null=True, blank=True)
    skip_count = models.IntegerField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    movement_number = models.IntegerField(null=True, blank=True)
    movement_count = models.IntegerField(null=True, blank=True)
    disc_number = models.IntegerField(null=True, blank=True)
    disc_count = models.IntegerField(null=True, blank=True)

    comments = models.CharField(blank=True, null=True, max_length=255)
    location = models.CharField(blank=True, null=True, max_length=255)
    grouping = models.CharField(blank=True, null=True, max_length=255)
    work = models.CharField(blank=True, null=True, max_length=255)
    movement_name = models.CharField(blank=True, null=True, max_length=255)
    location_escaped = models.CharField(blank=True, null=True, max_length=255)

    date_added = models.DateTimeField(blank=True, null=True)
    date_modified = models.DateTimeField(blank=True, null=True)
    lastplayed = models.DateTimeField(blank=True, null=True)
    skip_date = models.DateTimeField(blank=True, null=True)

    playlists = models.ManyToManyField(Playlist, blank=True)

    def get_artist(self):
        if self.artist:
            return self.artist
        elif self.album.artist:
            return self.album.artist
        else:
            return None

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['persistent_id', ]),
        ]
