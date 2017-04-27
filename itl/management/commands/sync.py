import os.path
import pickle
import time

from django.conf import settings
from django.core.management.base import BaseCommand

from itl.models import Artist, Album, Track, Genre, Kind

from pyItunes import Library


class Command(BaseCommand):
    help = "Synchronize iTunes Library with local database"

    def handle(self, *args, **options):

        lib_path = settings.LIBRARY_PATH
        pickle_file = "itl.p"
        expiry = 60 * 60  # Refresh pickled file if older than
        epoch_time = int(time.time())  # Now

        # Generate pickled version of database if stale or doesn't exist
        if not os.path.isfile(pickle_file) or os.path.getmtime(pickle_file) + expiry < epoch_time:
            itl_source = Library(lib_path)
            pickle.dump(itl_source, open(pickle_file, "wb"))
        itl = pickle.load(open(pickle_file, "rb"))

        #
        # for id, song in itl.songs.items():
        #     print("{n}, {r}".format(n=song.name, r=song.rating))

        playlists = itl.getPlaylistNames()
        for p in playlists:
            print(p)
        print("\n{c} playlists found".format(c=len(playlists)))

        print(playlists)

        '''
        ['album_rating', 'album_rating_computed', 'artist', 'bit_rate', 'comments', 'compilation', 'composer',
        'date_added', 'date_modified', 'disc_count', 'disc_number', 'genre', 'grouping', 'kind',
        'lastplayed', 'length', 'location', 'location_escaped', 'movement_count', 'movement_name',
        'movement_number', 'name', 'persistent_id', 'play_count', 'playlist_order', 'rating', 'rating_computed',
        'sample_rate', 'size', 'skip_count', 'skip_date', 'total_time', 'track_count', 'track_id', 'track_number',
        'track_type', 'work', 'year']
        '''

        for song in itl.getPlaylist('2016').tracks:
            print("[{t}] {a} - {n}".format(t=song.track_number, a=song.artist, n=song.name))

            if song.artist:
                artist, created = Artist.objects.get_or_create(name=song.artist)
            if song.album:
                album, created = Album.objects.get_or_create(title=song.album, artist=artist, year=song.year)
            if song.genre:
                genre, created = Genre.objects.get_or_create(name=song.genre)
            if song.kind:
                kind, created = Kind.objects.get_or_create(name=song.kind)

            track, created = Track.objects.get_or_create(
                title=song.name,
                artist=artist,
                album_artist=artist,
                composer=artist,
                year=song.year,
                loved=song.loved,
                album=album,
                genre=genre,
                kind=kind,
                size=song.size,
                bit_rate=song.bit_rate,
            )
