from django.shortcuts import render
from django.views import generic
from django.db.models.functions import Lower

from itl.models import Album, Track, Kind, Artist


def home(request):
    return render(request, 'home.html', locals(),)


class AlbumListView(generic.ListView):
    model = Album
    paginate_by = 100

    def get_queryset(self):
        return Album.objects.order_by(Lower('title'))


class AlbumDetailView(generic.DetailView):
    model = Album


class ArtistListView(generic.ListView):
    model = Artist
    paginate_by = 100

    def get_queryset(self):
        return Artist.objects.order_by(Lower('name'))


class ArtistDetailView(generic.DetailView):
    model = Artist


class TrackListView(generic.ListView):
    model = Track
    paginate_by = 100

    def get_queryset(self):
        return Track.objects.order_by(Lower('title'))


class TrackDetailView(generic.DetailView):
    model = Track


class KindListView(generic.ListView):
    model = Kind
    paginate_by = 100


class KindDetailView(generic.DetailView):
    model = Kind
