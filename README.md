# pyrex
Summary: Convert iTunes' XML "database" to a real Django database and project for advanced querying, analysis, data visualization.

Installation:
Django >= 1.11 is *required*.

pip install -r requirements.txt

Create a file `local.py` specifying the path to your iTunes XML file, e.g.:

`LIBRARY_PATH = "/Users/you/Music/iTunes/iTunes Library.xml"`

Create your postgres or mysql database, and add to your `local.py`:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pyrex',
        'USER': 'username',
        'PASSWORD': 'pass',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}
```

Unfortunately, sqlite3 is *not* supported by pyrex. I had originally intended to, but certain aspects of the sync process were extremely slow, and the optimization solution turned out not to work on sqlite ("too many variables" error). sync is around 3x faster on postgres with these optimizations, so it didn't seem worth the hit.

Interesting data point on the power of Django's `bulk_create()` method. If we use the naive `objects.create()` on each instance, time to populate the database with ~100k tracks on my machine is 34m41s. With `bulk_create()`, that number drops to 6 minutes. Unfortunately, there is no equivalent of `objects.get_or_create()` with `bulk_create()`, which means we'd end up with duplicates on every sync, unless we deleted all Track objects first on every run, which would nullify the benefit. So we don't use `bulk_create()`.

## Build your database

To set up tables in a default sqlite3 database, just run:

./manage.py migrate
./manage.py sync

Depending on the size of your collection, this could be a *long* process - for me, it takes around 30 minutes to catalog a 98,000-track library.
