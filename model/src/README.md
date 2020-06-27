# Model v2
This reimplements the surge model with simple dummy data

This uses Pipenv for managing packages because conda didn't install correctly an
does not deal with streamlit properly. Eventually we will move this to a docker
container

https://realpython.com/pipenv-guide/


# Logging

We define logging somewhat magically by using the same variable name and this
links all the logging togehter [Stackoverflow](https://stackoverflow.com/questions/40495083/using-python-logging-from-multiple-modules-with-writing-to-a-file-and-rotatingfi)

What this does is to create a logger with a different name from `__name__` in
each

```
import logging

log = logging.getLogger(__name__)
```

Then in the main executable is where you put the real work. This works because
the hierarchy means that when a module is called, takes the parameters from the
parent which is in main.

```
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
```