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
        #
        # # for song in itl.getPlaylist('GD Best').tracks:
        # for id, song in itl.songs.items():
        #     try:
        #         print("{a} - {n}".format(a=song.artist, n=song.name))
        #     except:
        #         print("Track missing metadata")
        #
        #     artist = album = genre = kind = None
        #
        #     if song.artist or song.album_artist:
        #         artist_str = song.artist or song.album_artist
        #         artist, created = Artist.objects.get_or_create(name=artist_str)
        #
        #     if song.album:
        #         # Quasi-bug: Each song will reset year on album, which may not be correct
        #         album, created = Album.objects.get_or_create(
        #             title=song.album,
        #             defaults={'artist': artist, 'year': song.year})
        #
        #     if song.genre:
        #         genre, created = Genre.objects.get_or_create(name=song.genre)
        #
        #     if song.kind:
        #         kind, created = Kind.objects.get_or_create(name=song.kind)
        #
        #     track_data = {
        #         'title': song.name,
        #         'artist': artist,
        #         'composer': artist,
        #         'year': song.year,
        #         'loved': song.loved,
        #         'album': album,
        #         'genre': genre,
        #         'kind': kind,
        #         'size': song.size,
        #         'bit_rate': song.bit_rate,
        #     }
        #     # tracks.append(Track(**data))
        #     track, created = Track.objects.update_or_create(
        #         persistent_id=song.persistent_id,
        #         defaults=track_data,
        #     )

        # Create playlists
        playlists = itl.getPlaylistNames()
        # playlists = [itl.getPlaylist('GD Best'), ]
        print("\n{c} playlists found".format(c=len(playlists)))
        for p in playlists:
            playlist, created = Playlist.objects.get_or_create(name=p)
            if created:
                print("Created playlist {0}".format(playlist.name))
            print("Adding tracks to playlist {0}".format(playlist.name))
            # In case tracks were deleted or re-ordered since last sync, delete and re-create all track refs
            playlist.track_set.clear()
            playlist_name = itl.getPlaylist(p)
            for t in playlist_name.tracks:
                track = Track.objects.get(persistent_id=t.persistent_id)
                playlist.track_set.add(track)
