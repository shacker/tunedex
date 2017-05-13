from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Lower
from django.shortcuts import render, get_object_or_404
from django.views import generic

from itl.models import Album, Track, Kind, Artist, Playlist


def dashboard(request):
    artists_count = Artist.objects.all().count()
    albums_count = Album.objects.all().count()
    tracks_count = Track.objects.all().count()
    playlists_count = Playlist.objects.all().count()
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


def track_detail(request, pid=None):
    track = get_object_or_404(Track, persistent_id=pid)

    return render(request, 'itl/track_detail.html', locals())


class KindListView(generic.ListView):
    model = Kind
    paginate_by = 100


class KindDetailView(generic.DetailView):
    model = Kind


class PlaylistListView(generic.ListView):
    model = Playlist


def playlist_detail(request, pk=None):

    playlist = get_object_or_404(Playlist, pk=pk)
    playlist_tracks = playlist.track_set.all()
    paginator = Paginator(playlist_tracks, 25)
    page = request.GET.get('page')

    try:
        tracks = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tracks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tracks = paginator.page(paginator.num_pages)

    return render(request, 'itl/playlist_detail.html', locals())
