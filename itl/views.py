from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Lower
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q

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
        tracks = self.object.track_set.all().order_by('disc_number', 'track_number')
        context['tracks'] = tracks
        context['multidisc'] = True if len(set([t.disc_number for t in tracks])) > 1 else False
        return context


class ArtistListView(generic.ListView):
    model = Artist
    paginate_by = 100

    def get_queryset(self):
        return Artist.objects.order_by(Lower('name'))


def artist_detail(request, pk=None):
    artist = get_object_or_404(Artist, pk=pk)
    albums = Album.objects.filter(artist=artist).order_by('-year')
    tracks = artist.track_set.all()
    return render(request, 'itl/artist_detail.html', locals())


def track_list(request):

    # For select dropdowns. n.b. kinds is respected in queries but not shown as dropdown or column
    genres = Genre.objects.all().order_by('name')
    years = Track.objects.exclude(year=None).order_by('-year').values_list('year', flat=True).distinct()
    kinds = Kind.objects.all().order_by('name')

    qs = Track.objects.all().order_by(Lower('title'))
    year = request.GET.get('year')
    genre = request.GET.get('genre')
    kind = request.GET.get('kind')
    q = request.GET.get('q')
    if q:

        # SearchVector with annotate is slow for now: https://code.djangoproject.com/ticket/27719
        # from django.contrib.postgres.search import SearchVector
        # qs = Track.objects.select_related('artist').select_related('album').select_related('genre').annotate(search=SearchVector(
        #     'title', 'comments', 'artist__name', 'album__title')).filter(search=q)

        qs = Track.objects.select_related('artist').select_related('album').select_related('genre').filter(
            Q(title__icontains=q) |
            Q(comments__icontains=q) |
            Q(artist__name__icontains=q) |
            Q(album__title__icontains=q)
        )

    if year:
        year = int(year)
        qs = qs.filter(year=year)
    if genre:
        genre = int(genre)
        qs = qs.filter(genre__id=genre)
    if kind:
        kind = int(kind)
        qs = qs.filter(kind__id=kind)

    qs = qs.order_by('title')

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


class PlaylistListView(generic.ListView):
    model = Playlist
    paginate_by = 50


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


def genres_donut(request):
    return render(request, 'itl/chart_genres_donut.html', locals())


def kinds_donut(request):
    return render(request, 'itl/chart_kinds_donut.html', locals())


def most_played_bar(request):
    return render(request, 'itl/chart_most_played_bar.html', locals())


def kinds_area(request):
    return render(request, 'itl/chart_kinds_area.html', locals())
