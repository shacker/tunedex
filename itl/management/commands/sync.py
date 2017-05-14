import datetime
import os.path
import pickle
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from pyItunes import Library

from itl.models import Artist, Album, Track, Genre, Kind, TrackType, Playlist


class Command(BaseCommand):
    help = "Synchronize iTunes Library with local database"

    def struct_to_datetime(self, struct_time):
        '''
        iTunes stores timestamps as struct_time fields, but in Django we're using DateTime fields.
        Convert if possible, or return None.
        '''
        if struct_time:
            return timezone.make_aware(datetime.datetime.fromtimestamp(time.mktime(struct_time)))
        else:
            return None

    def add_arguments(self, parser):
        parser.add_argument('playlist_args', nargs='?', type=str)

    def handle(self, *args, **options):

        lib_path = settings.LIBRARY_PATH

        # Use pickled version of xml db for repeat runs, if available, or generate
        pickle_file = "itl.p"
        expiry = 60 * 60 * 24 * 30  # Refresh pickled file if older than
        epoch_time = int(time.time())  # Now
        if not os.path.isfile(pickle_file) or os.path.getmtime(pickle_file) + expiry < epoch_time:
            itl_source = Library(lib_path)
            pickle.dump(itl_source, open(pickle_file, "wb"))
        itl = pickle.load(open(pickle_file, "rb"))

        # Either take playlist names from cli args, or get all
        playlists = options['playlist_args'].split(",") if options['playlist_args'] else itl.getPlaylistNames()

        for pl in playlists:
            print(pl)
            for song in itl.getPlaylist(pl).tracks:
                try:
                    print("{a} - {n}".format(a=song.artist, n=song.name))
                except:
                    print("Track missing metadata")

                artist = album = genre = kind = None

                if song.artist or song.album_artist:
                    artist_str = song.artist or song.album_artist
                    artist, created = Artist.objects.get_or_create(name=artist_str)

                if song.album:
                    # Quasi-bug: Each song will reset year and rating on album, which may not be correct
                    album, created = Album.objects.get_or_create(
                        title=song.album,
                        defaults={'artist': artist, 'year': song.year, 'album_rating': song.album_rating})

                if song.genre:
                    genre, created = Genre.objects.get_or_create(name=song.genre)

                if song.track_type:
                    track_type, created = TrackType.objects.get_or_create(name=song.track_type)

                if song.kind:
                    kind, created = Kind.objects.get_or_create(name=song.kind)

                track_data = {
                    'track_id': song.track_id,
                    'title': song.name,
                    'artist': artist,
                    'composer': artist,
                    'year': song.year,
                    'loved': song.loved,
                    'compilation': song.compilation,
                    'album': album,
                    'genre': genre,
                    'kind': kind,
                    'track_type': track_type,
                    'size': song.size,
                    'bit_rate': song.bit_rate,
                    'total_time': song.total_time,
                    'track_number': song.track_number,
                    'track_count': song.track_count,
                    'sample_rate': song.sample_rate,
                    'rating': song.rating,
                    'play_count': song.play_count,
                    'skip_count': song.skip_count,
                    'length': song.length,
                    'movement_number': song.movement_number,
                    'movement_count': song.movement_count,
                    'disc_number': song.disc_number,
                    'disc_count': song.disc_count,
                    'comments': song.comments,
                    'grouping': song.grouping,
                    'work': song.work,
                    'movement_name': song.movement_name,
                    'date_added': self.struct_to_datetime(song.date_added),
                    'date_modified': self.struct_to_datetime(song.date_modified),
                    'lastplayed': self.struct_to_datetime(song.lastplayed),
                    'skip_date': self.struct_to_datetime(song.skip_date),
                }

                track, created = Track.objects.update_or_create(
                    persistent_id=song.persistent_id,
                    defaults=track_data,
                )

        # Create playlists
        plists = [itl.getPlaylist(p) for p in playlists]
        print("\n{c} playlists found".format(c=len(plists)))
        for pl in plists:
            playlist_name = pl.name
            playlist, created = Playlist.objects.get_or_create(name=playlist_name)
            print("Adding tracks to playlist {0}".format(playlist_name))
            persistent_ids = [t.persistent_id for t in pl.tracks]
            addtraks = Track.objects.filter(persistent_id__in=persistent_ids)
            playlist.track_set.set(addtraks, clear=True)
