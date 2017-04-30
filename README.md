# pyrex
Convert iTunes database to a Django project for advanced querying, analysis

We default to sqlite for simplicity. Of course you can use postgres or mysql if you prefer  - just modify the DATABASES dict in settings.

Create a file `local.py` specifying the path to your iTunes XML file, e.g.:

`LIBRARY_PATH = "/Users/you/Music/iTunes/iTunes Library.xml"`
