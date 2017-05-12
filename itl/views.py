from django.shortcuts import render
from django.db.models.functions import Lower
from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView

from itl.models import Album, Track, Kind, Artist, Playlist


def dashboard(request):
    artists_count = Artist.objects.all().count()
    albums_count = Album.objects.all().count()
    tracks_count = Track.objects.all().count()
    playlists_count = 17
    return render(request, 'dashboard.html', locals(),)


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


class PlaylistListView(generic.ListView):
    model = Playlist


class PlaylistDetailView(SingleObjectMixin, ListView):
    model = Playlist

    paginate_by = 100
    template_name = "itl/playlist_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Playlist.objects.all())
        return super(PlaylistDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PlaylistDetailView, self).get_context_data(**kwargs)
        context['playlist'] = self.object
        return context

    def get_queryset(self):
        return self.object.track_set.all()
