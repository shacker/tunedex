from django.conf.urls import include, url
from django.contrib import admin

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

    # Charts
    url(r'^charts/genres_donut/$', views.genres_donut, name='genres_donut'),
    url(r'^charts/kinds_donut/$', views.kinds_donut, name='kinds_donut'),
    url(r'^charts/most_played_bar/$', views.most_played_bar, name='most_played_bar'),
    url(r'^charts/kinds_area/$', views.kinds_area, name='kinds_area'),
    url(r'^charts/years_cloud/$', views.years_cloud, name='years_cloud'),
    url(r'^charts/artists_pie/$', views.artists_pie, name='artists_pie'),

    # JSON views
    url(r'^json/genres_data/(?P<num_genres>\d+)/$', json_views.genres_data, name='genres_data'),
    url(r'^json/genres_data/$', json_views.genres_data, name='genres_data'),
    url(r'^json/kinds_data/(?P<num_kinds>\d+)/$', json_views.kinds_data, name='kinds_data'),
    url(r'^json/most_played_data/(?P<num_tracks>\d+)/$', json_views.most_played_data, name='most_played_data'),
    url(r'^json/media_formats_data/$', json_views.media_formats, name='media_formats'),
    url(r'^json/years_data/$', json_views.years_data, name='years_data'),
    url(r'^json/artists_pie/$', json_views.artists_data, name='artists_pie_data'),

    url(r'^admin/', admin.site.urls),
]


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
