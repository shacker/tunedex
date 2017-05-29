from django.http import JsonResponse
from django.db.models import Count

from itl.models import Genre


def dashboard_genres_donut_data(request):
    # Generate data to show top 5 genres on dashboard
    genres = Genre.objects.annotate(num_tracks=Count('track')).order_by('-num_tracks')[:5]
    data = [{"label": g.name, "value": g.num_tracks} for g in genres]

    return JsonResponse(data, safe=False)
