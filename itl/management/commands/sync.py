import os.path
import pickle
import time

from django.conf import settings
from django.core.management.base import BaseCommand

from itl.models import Artist, Album, Track, Genre, Kind, Playlist

from pyItunes import Library


class Command(BaseCommand):
    help = "Synchronize iTunes Library with local database"

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
        theset = ['GD Best', ]
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
                    # Quasi-bug: Each song will reset year on album, which may not be correct
                    album, created = Album.objects.get_or_create(
                        title=song.album,
                        defaults={'artist': artist, 'year': song.year})

                if song.genre:
                    genre, created = Genre.objects.get_or_create(name=song.genre)

                if song.kind:
                    kind, created = Kind.objects.get_or_create(name=song.kind)

                track_data = {
                    'title': song.name,
                    'artist': artist,
                    'composer': artist,
                    'year': song.year,
                    'loved': song.loved,
                    'album': album,
                    'genre': genre,
                    'kind': kind,
                    'size': song.size,
                    'bit_rate': song.bit_rate,
                }
                track, created = Track.objects.update_or_create(
                    persistent_id=song.persistent_id,
                    defaults=track_data,
                )

        # Create playlists
        # playlists = itl.getPlaylistNames()
        # playlists = [itl.getPlaylist('GD Best'), itl.getPlaylist('Compilations'), itl.getPlaylist('Decade 1970s'), ]
        playlists = [itl.getPlaylist('GD Best'), ]
        print("\n{c} playlists found".format(c=len(playlists)))
        for p in playlists:
            playlist_name = p.name
            playlist, created = Playlist.objects.get_or_create(name=playlist_name)
            print("Adding tracks to playlist {0}".format(playlist_name))
            persistent_ids = [t.persistent_id for t in p.tracks]
            addtraks = Track.objects.filter(persistent_id__in=persistent_ids)
            playlist.track_set.set(addtraks, clear=True)
