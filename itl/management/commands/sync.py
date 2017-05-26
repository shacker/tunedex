import datetime
import os.path
import pickle
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.utils import DataError

from libpytunes import Library

from itl.models import Artist, Album, Track, Genre, Kind, TrackType, Playlist, PlaylistEntry, LibraryData


class Command(BaseCommand):
    help = "Synchronize iTunes Library with local database. Pass in limit as int to process partial library."

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
        parser.add_argument('limit', nargs='?', type=int)

    def handle(self, *args, **options):

        lib_path = settings.LIBRARY_PATH

        if settings.DEBUG:
            # Use pickled version of xml db for repeat runs, if available, or generate
            pickle_file = "itl.p"
            expiry = settings.PICKLE_AGE  # Refresh pickled file if older than
            epoch_time = int(time.time())  # Now
            if not os.path.isfile(pickle_file) or os.path.getmtime(pickle_file) + expiry < epoch_time:
                itl_source = Library(lib_path)
                pickle.dump(itl_source, open(pickle_file, "wb"))
            itl = pickle.load(open(pickle_file, "rb"))
        else:
            itl = Library(lib_path)
        self.itl = itl

        self.import_songs(**options)
        self.import_playlists(**options)
        self.update_snapshot()

    def import_songs(self, **options):
        '''
        Import all songs in library XMl.
        '''

        itl = self.itl
        # Optionally limit to a partial lib for testing
        limit = options['limit'] if options['limit'] else 99999999999999
        songcount = len(itl.songs)

        for index, song in enumerate(itl.songs.items()):
            if index > limit:
                break

            # song obj is now e.g. `(15607, <pyItunes.Song.Song object at 0x109473e48>)``
            song = song[1]

            print("{index}/{sc} {a} - {n}".format(a=song.artist, n=song.name, index=index, sc=songcount))

            artist = album = genre = kind = None

            if song.artist or song.album_artist:
                artist_str = song.artist or song.album_artist
                artist, created = Artist.objects.get_or_create(name=artist_str)

            if song.album:
                # Quasi-bug: Each song will reset year and rating on album, which may or may not be correct
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
                'album': album,
                'artist': artist,
                'bit_rate': song.bit_rate,
                'comments': song.comments,
                'compilation': song.compilation,
                'composer': artist,
                'date_added': self.struct_to_datetime(song.date_added),
                'date_modified': self.struct_to_datetime(song.date_modified),
                'disc_count': song.disc_count,
                'disc_number': song.disc_number,
                'genre': genre,
                'grouping': song.grouping,
                'kind': kind,
                'lastplayed': self.struct_to_datetime(song.lastplayed),
                'length': song.length,
                'loved': song.loved,
                'movement_count': song.movement_count,
                'movement_name': song.movement_name,
                'movement_number': song.movement_number,
                'play_count': song.play_count,
                'rating': song.rating,
                'sample_rate': song.sample_rate,
                'size': song.size,
                'skip_count': song.skip_count,
                'skip_date': self.struct_to_datetime(song.skip_date),
                'total_time': song.total_time,
                'title': song.name,
                'track_count': song.track_count,
                'track_id': song.track_id,
                'track_number': song.track_number,
                'track_type': track_type,
                'work': song.work,
                'year': song.year,
            }

            try:
                track, created = Track.objects.update_or_create(
                    persistent_id=song.persistent_id,
                    defaults=track_data,
                )
            except DataError:
                # Probably a video file, too large to fit into Django IntegerField.
                # Because this is a rare exception, deciding to skip rather than use BigIntegerField everywhere.
                pass

    def import_playlists(self, **options):
        '''
        Create playlists, emptying old ones first
        '''

        itl = self.itl
        PlaylistEntry.objects.all().delete()
        plists = [itl.getPlaylist(p) for p in itl.getPlaylistNames()]
        # plists = [itl.getPlaylist("foo"), ]
        print("\n{c} playlists found".format(c=len(plists)))
        for pl in plists:
            entries = []
            playlist, created = Playlist.objects.get_or_create(name=pl.name)
            print("Adding tracks to playlist {0}".format(pl.name))
            for itl_trak in pl.tracks:
                entries.append(PlaylistEntry(
                    track=Track.objects.get(persistent_id=itl_trak.persistent_id),
                    playlist=playlist,
                    playlist_order=itl_trak.playlist_order
                    )
                )
            PlaylistEntry.objects.bulk_create(entries)

    def update_snapshot(self):
        # Update snapshot datetime
        sitemeta, created = LibraryData.objects.get_or_create(pk=1)
        sitemeta.last_snapshot = timezone.now()
        sitemeta.save()
