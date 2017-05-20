from django.contrib import admin
from itl.models import Album, Artist, Genre, Track, Kind


class AlbumAdmin(admin.ModelAdmin):
    raw_id_fields = ["artist", ]
    list_display = ['title', 'artist', 'year', ]
    search_fields = ['title', 'artist__name', 'year', ]
    ordering = ['title', ]


class TrackAdmin(admin.ModelAdmin):
    raw_id_fields = ["artist", "album", ]
    list_display = ['title', 'artist', 'album', 'year', ]
    search_fields = ['title', 'artist__name', 'year', ]
    ordering = ['title', ]


class GenreAdmin(admin.ModelAdmin):
    ordering = ['name', ]


class KindAdmin(admin.ModelAdmin):
    ordering = ['name', ]


admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Kind, KindAdmin)
admin.site.register(Track, TrackAdmin)
