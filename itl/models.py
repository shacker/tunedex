from django.db import models


class Artist(models.Model):
    name = models.CharField(default="Artist Unknown", max_length=255)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(default="Album Unknown", max_length=255)
    artist = models.ForeignKey(Artist, null=True, blank=True, on_delete=models.SET_NULL)
    year = models.PositiveSmallIntegerField(null=True, blank=True)

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


class Track(models.Model):
    persistent_id = models.CharField(max_length=255, blank=True)
    title = models.CharField(default="Unknown", max_length=255)
    artist = models.ForeignKey(Artist, blank=True, null=True)
    composer = models.ForeignKey(Artist, blank=True, null=True, related_name="track_composer")
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    album = models.ForeignKey(Album, blank=True, null=True)
    genre = models.ForeignKey(Genre, blank=True, null=True)
    kind = models.ForeignKey(Kind, blank=True, null=True)
    size = models.IntegerField(null=True, blank=True)
    bit_rate = models.IntegerField(null=True, blank=True)
    loved = models.BooleanField(default=False)

    def get_artist(self):
        if self.artist:
            return self.artist
        elif self.album.artist:
            return self.album.artist
        else:
            return None

    def __str__(self):
        return self.title

# Add LOVED
# total_time = None (Integer)
# track_number = None (Integer)
# track_count = None (Integer)
# disc_number = None (Integer)
# disc_count = None (Integer)
# date_modified = None (Time)
# date_added = None (Time)
# sample_rate = None (Integer)
# comments = None (String)
# rating = None (Integer)
# album_rating = None (Integer)
# play_count = None (Integer)
# location = None (String)
# location_escaped = None (String)
# compilation = None (Boolean)
# grouping = None (String)
# lastplayed = None (Time)
# skip_count = None (Integer)
# skip_date = None(Time)
# length = None (Integer)
# work = None (String)
# movement_name = None (String)
# movement_number = None (Integer)
# movement_count = None (Integer)
