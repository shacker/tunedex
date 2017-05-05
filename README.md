# pyrex
Convert iTunes database to a Django project for advanced querying, analysis

We default to sqlite for simplicity. Of course you can use postgres or mysql if you prefer  - just modify the DATABASES dict in settings.

Create a file `local.py` specifying the path to your iTunes XML file, e.g.:

`LIBRARY_PATH = "/Users/you/Music/iTunes/iTunes Library.xml"`

Interesting data point on the power of Django's `bulk_create()` method. If we use the naive `objects.create()` on each instance, time to populate the database with ~100k tracks on my machine is 34m41s. With `bulk_create()`, that number drops to 6 minutes. Unfortunately, there is no equivalent of `objects.get_or_create()` with `bulk_create()`, which means we'd end up with duplicates on every sync, unless we deleted all Track objects first on every run, which would nullify the benefit. So we don't use `bulk_create()`.

## Build your database

To set up tables in a default sqlite3 database, just run:

./manage.py migrate
./manage.py sync

Depending on the size of your collection, this could be a *long* process - for me, it takes around 30 minutes to catalog a 98,000-track library.

If you prefer to use postgres or mysql, do something like this in your `local.py` (though there's not much reason to use anything but sqlite for this application):
