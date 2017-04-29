from django.shortcuts import render
from django.views import generic
from django.db.models.functions import Lower


from itl.models import Album, Track


def home(request):
    return render(request, 'home.html', locals(),)


class AlbumListView(generic.ListView):
    model = Album

    def get_queryset(self):
        return Album.objects.order_by(Lower('title'))


class AlbumDetailView(generic.DetailView):
    model = Album


class TrackListView(generic.ListView):
    model = Track

    def get_queryset(self):
        return Track.objects.order_by(Lower('title'))


class TrackDetailView(generic.DetailView):
    model = Track
