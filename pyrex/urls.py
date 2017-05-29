from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from itl import views
from itl import json_views as json_views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^albums/$', views.AlbumListView.as_view(), name='albums'),
    url(r'^albums/(?P<pk>\d+)$', views.AlbumDetailView.as_view(), name='album_detail'),

    url(r'^artists/$', views.ArtistListView.as_view(), name='artists'),
    url(r'^artists/(?P<pk>\d+)$', views.artist_detail, name='artist_detail'),

    url(r'^tracks/$', views.track_list, name='tracks'),
    url(r'^tracks/(?P<pid>\w+)$', views.track_detail, name='track_detail'),

    url(r'^playlists/$', views.PlaylistListView.as_view(), name='playlists'),
    url(r'^playlists/(?P<pk>\d+)$', views.playlist_detail, name='playlist_detail'),

    # JSON views

    url(r'^json/dashboard_genres_donut_data/$', json_views.dashboard_genres_donut_data, name='dashboard_genres_donut_data'),


    url(r'^admin/', admin.site.urls),
]


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
