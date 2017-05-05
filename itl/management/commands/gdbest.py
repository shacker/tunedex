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

        pickle_file = "itl.p"
        itl = pickle.load(open(pickle_file, "rb"))


        for song in itl.getPlaylist('GD Best').tracks:
        # tracks = []
        # for id, song in itl.songs.items():
            try:
                print("{a} - {n}".format(a=song.artist, n=song.name))
            except:
                print("Track missing metadata")
