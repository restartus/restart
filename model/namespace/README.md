# Testing of namespaces and packages
[Sudonull](https://sudonull.com/post/25978-Combining-multiple-packages-into-a-single-Python-namespace) explains how to do this.

## Native namespace

As [Native namespace packages](https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages)
the main thing is to make sure that you do not have an __init__.py or it will
fail which means that setuptools.find_packages won't find them so you need to
run setuptools.find_namespace_packages in setup.py to get them
