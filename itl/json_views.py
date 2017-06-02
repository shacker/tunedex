from django.http import JsonResponse
from django.db.models import Count

from itl.models import Genre


def genres_data(request, num_genres=None):
    # Generate data to show top 5 genres on dashboard
    num_genres = int(num_genres) if num_genres else 10
    genres = Genre.objects.annotate(num_tracks=Count('track')).order_by('-num_tracks')[:num_genres]
    data = [{"label": g.name, "value": g.num_tracks, "id": g.id} for g in genres]

    return JsonResponse(data, safe=False)
