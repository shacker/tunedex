from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Lower
from django.shortcuts import render, get_object_or_404
from django.views import generic

from itl.models import Album, Track, Kind, Artist, Playlist, LibraryData, Genre


def dashboard(request):
    artists_count = Artist.objects.all().count()
    albums_count = Album.objects.all().count()
    tracks_count = Track.objects.all().count()
    playlists_count = Playlist.objects.all().count()
    sitemeta, created = LibraryData.objects.get_or_create(pk=1)
    return render(request, 'dashboard.html', locals(),)


class AlbumListView(generic.ListView):
    model = Album
    paginate_by = 100

    def get_queryset(self):
        return Album.objects.order_by(Lower('title'))


class AlbumDetailView(generic.DetailView):
    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tracks = self.object.track_set.all().order_by('track_number')
        context['tracks'] = tracks
        return context


class ArtistListView(generic.ListView):
    model = Artist
    paginate_by = 100

    def get_queryset(self):
        return Artist.objects.order_by(Lower('name'))


class ArtistDetailView(generic.DetailView):
    model = Artist


def track_list(request):

    # For select dropdowns
    genres = Genre.objects.all().order_by('name')
    years = Track.objects.exclude(year=None).order_by('-year').values_list('year', flat=True).distinct()
    kinds = Kind.objects.all().order_by('name')

    qs = Track.objects.all().order_by(Lower('title'))
    year = request.GET.get('year')
    genre = request.GET.get('genre')
    kind = request.GET.get('kind')
    if year:
        year = int(year)
        qs = qs.filter(year=year)
    if genre:
        genre = int(genre)
        qs = qs.filter(genre__id=genre)
    if kind:
        kind = int(kind)
        qs = qs.filter(kind__id=kind)

    paginator = Paginator(qs, settings.NUM_TRACKS_PER_PLAYLIST_PAGE)
    page = request.GET.get('page', 1)

    try:
        tracks = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tracks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tracks = paginator.page(paginator.num_pages)

    return render(request, 'itl/track_list.html', locals())


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
    paginate_by = 25


def playlist_detail(request, pk=None):

    playlist = get_object_or_404(Playlist, pk=pk)
    playlist_tracks = playlist.playlistentry_set.all().order_by('playlist_order')
    paginator = Paginator(playlist_tracks, settings.NUM_TRACKS_PER_PLAYLIST_PAGE)
    page = request.GET.get('page', 1)

    try:
        tracks = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tracks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tracks = paginator.page(paginator.num_pages)

    return render(request, 'itl/playlist_detail.html', locals())
