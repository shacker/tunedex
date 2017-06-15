from django.http import JsonResponse
from django.db.models import Count

from itl.models import Genre, Kind, Track, Year


def genres_data(request, num_genres=None):
    # Generate data to show top genres
    num_genres = int(num_genres) if num_genres else 10
    genres = Genre.objects.annotate(num_tracks=Count('track')).order_by('-num_tracks')[:num_genres]
    data = [{"label": g.name, "value": g.num_tracks, "id": g.id} for g in genres]

    return JsonResponse(data, safe=False)


def kinds_data(request, num_kinds=None):
    # Generate data to show top kinds
    num_kinds = int(num_kinds) if num_kinds else 10
    kinds = Kind.objects.annotate(num_kinds=Count('track')).order_by('-num_kinds')[:num_kinds]
    data = [{"label": k.name, "value": k.num_kinds, "id": k.id} for k in kinds]

    return JsonResponse(data, safe=False)


def most_played_data(request, num_tracks=None):
    # Generate data to show top kinds
    num_tracks = int(num_tracks) if num_tracks else 10
    tracks = Track.objects.exclude(play_count__isnull=True).order_by('-play_count')[:num_tracks]
    data = [{
        "title": t.title,
        "artist": t.artist.name,
        "plays": t.play_count,
        "persistent_id": t.persistent_id
        } for t in tracks
    ]

    return JsonResponse(data, safe=False)


def media_formats(request):
    # Generate data to show media formats
    # Get all years for which new media was added, and all formats in use:
    years_qs = Track.objects.all().dates('date_added', 'year')
    years = sorted(list(set([y.year for y in years_qs])))
    formats = Kind.objects.all()

    datasets = []
    for f in formats:
        track_data = [Track.objects.filter(kind=f, date_added__year=y).count() for y in years]
        datasets.append({"label": f.name, "data": track_data})

    data = {
        'labels': years,
        'datasets': datasets
    }

    return JsonResponse(data, safe=False)


def years_data(request):
    # Generate data to show most popular years
    years = Year.objects.annotate(num_tracks=Count('track')).order_by('-num_tracks')

    '''
    data = [
      {"year": "1981", "num_tracks": 13, "link": 'http://github.com/mistic100/jQCloud'},
      {"year": "1965", "num_tracks": 10.5, "link": 'http://www.strangeplanet.fr'},
      {"year": "2017", "num_tracks": 9.4, "link": 'http://piwigo.org'},
    ]
    '''

    data = []
    for year in years:
        data.append({"text": year.id, "weight": year.num_tracks, "link": "/tracks/?year={}".format(year.id)})

    return JsonResponse(data, safe=False)
