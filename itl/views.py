from django.shortcuts import render
from django.views import generic
from django.db.models.functions import Lower


from itl.models import Album


def home(request):
    return render(request, 'home.html', locals(),)


class AlbumListView(generic.ListView):
    model = Album

    def get_queryset(self):
        return Album.objects.order_by(Lower('title'))


class AlbumDetailView(generic.DetailView):
    model = Album
