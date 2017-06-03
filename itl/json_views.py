from django.http import JsonResponse
from django.db.models import Count

from itl.models import Genre, Kind, Track


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
    # tracks = Track.objects.annotate(num_plays=Count('play_count')).order_by('-play_count')[:num_tracks]
    tracks = Track.objects.exclude(play_count__isnull=True).order_by('-play_count')[:num_tracks]
    data = [{
        "title": t.title,
        "artist": t.artist.name,
        "plays": t.play_count,
        "persistent_id": t.persistent_id
        } for t in tracks
    ]

    return JsonResponse(data, safe=False)
