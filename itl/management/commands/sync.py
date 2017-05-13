import os.path
import pickle
import time
from time import mktime

from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from itl.models import Artist, Album, Track, Genre, Kind, TrackType, Playlist

from pyItunes import Library


class Command(BaseCommand):
    help = "Synchronize iTunes Library with local database"

    def struct_to_datetime(self, struct_time):
        '''
        iTunes stores timestamps as struct_time fields, but in Django we're using DateTime fields.
        Convert if possible, or return None.
        '''
        if struct_time:
            return timezone.make_aware(datetime.fromtimestamp(mktime(struct_time)))
        else:
            return None

    def handle(self, *args, **options):

        lib_path = settings.LIBRARY_PATH
        pickle_file = "itl.p"
        expiry = 60 * 60 * 24 * 30  # Refresh pickled file if older than
        epoch_time = int(time.time())  # Now

        # Generate pickled version of database if stale or doesn't exist
        if not os.path.isfile(pickle_file) or os.path.getmtime(pickle_file) + expiry < epoch_time:
            itl_source = Library(lib_path)
            pickle.dump(itl_source, open(pickle_file, "wb"))
        itl = pickle.load(open(pickle_file, "rb"))

        '''
        ['album_rating', 'album_rating_computed', 'artist', 'bit_rate', 'comments', 'compilation', 'composer',
        'date_added', 'date_modified', 'disc_count', 'disc_number', 'genre', 'grouping', 'kind',
        'lastplayed', 'length', 'location', 'location_escaped', 'movement_count', 'movement_name',
        'movement_number', 'name', 'persistent_id', 'play_count', 'playlist_order', 'rating', 'rating_computed',
        'sample_rate', 'size', 'skip_count', 'skip_date', 'total_time', 'track_count', 'track_id', 'track_number',
        'track_type', 'work', 'year']
        '''

        # for id, song in itl.songs.items():

        # theset = ['Decade 1970s', 'Compilations', 'GD Best', ]
        theset = ['Beatles Black Album', ]
        for pl in theset:
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
                    'location': song.location,
                    'grouping': song.grouping,
                    'work': song.work,
                    'movement_name': song.movement_name,
                    'location_escaped': song.location_escaped,

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
        # playlists = itl.getPlaylistNames()
        # playlists = [itl.getPlaylist('GD Best'), itl.getPlaylist('Compilations'), itl.getPlaylist('Decade 1970s'), ]
        playlists = [itl.getPlaylist('Beatles Black Album'), ]
        print("\n{c} playlists found".format(c=len(playlists)))
        for p in playlists:
            playlist_name = p.name
            playlist, created = Playlist.objects.get_or_create(name=playlist_name)
            print("Adding tracks to playlist {0}".format(playlist_name))
            persistent_ids = [t.persistent_id for t in p.tracks]
            addtraks = Track.objects.filter(persistent_id__in=persistent_ids)
            playlist.track_set.set(addtraks, clear=True)
