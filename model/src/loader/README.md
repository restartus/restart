# Loader library

To create a subdirectory that is referrable we are making a 'faux' package as
[described](https://stackoverflow.com/questions/1260792/import-a-file-from-a-subdirectory)
and
you don't need an __init__.py for versions before Python 3.3 previously. And now
you should *not* have this __init__.py so that you have use namespaces
