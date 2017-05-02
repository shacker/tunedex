# pyrex
Convert iTunes database to a Django project for advanced querying, analysis

We default to sqlite for simplicity. Of course you can use postgres or mysql if you prefer  - just modify the DATABASES dict in settings.

Create a file `local.py` specifying the path to your iTunes XML file, e.g.:

`LIBRARY_PATH = "/Users/you/Music/iTunes/iTunes Library.xml"`

Interesting data point on the power of Django's `bulk_create()` method. If we use the naive `objects.create()` on each instance, time to populate the database with ~100k tracks on my machine is 34m41s. With `bulk_create()`, that number drops to 6 minutes.
