# Super frustrated with logging

The documentation on best practices is extremely poor plus logging does not seem
to work correct across modules, so this is test scaffolding.

Using the core documents for Python 3.8
[Logging](https://docs.python.org/3/howto/logging.html)

The basic learning is that the first example says you should always have a
custom logging object

```
import logging
log = logging.getLogger(__name__)
```

The thing that it doesn't tel you is that this logger is unconnected to any
module. There doesn't seem to be a hierarchy of loggers, so you have to manage
each one.

The default is that you can use it directly and not create any objects with

```python
logging.warning('help!')
```

Note that the default is that only warnings and above come out.

## Logging levels in two different places at Logging and Handler

The second trick is that log levels are set at the Logger level and the Handler
level, so you have to set both. This is because you can have multiple handlers
so that some events go to the console (real Warnings) and others go to files
(you can set debug there). As the [Logging
cookbook](https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook)
shows

[Advanced](https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial)
the advanced guide talks in detail about how the Logger first sees the event and
decides if it should reject because it's too low level or not or if there is a
filter. Then each handler is called and they do their own filterng.

There are also a sea of handlers, such as `RotatingFileHandler` so you don't get
gigantic logfiles

## Cascading handlers

The way around this is to use the dot notation with handlers, so for instance
there is inheritance like this

```
log = logging.getLogger('__main__.' + __name__)
```

You can even do this per class and stuff a logger underneath so in a class file

```
import logging

log_name = '__main__' + __name__
log = logging.getLogger(log_name)

# https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook
class new_class:
    def init(self):
        self.logger = logging.getLogger(log_name + type(self).__name__)
```

This will bind the current module to the logger that is active with
`__main__`

## Logginer names are the same

This is a really important point, if you call says

```
log = logging.getLogger('hello')
```

Multiple times, it is always the same handler, so one simple trick is to not do
the `getLogger(__name__)` and just use the same name for your entire project.


## How to avoid configure the loggers everytime

Because the best practice is to have a separate logger for each module (file).
You can be pretty selective, but it also requires a lot of boiler plate since
you have to set the file handlers and stream handlers each time.


## Moving the configuration from the code to a YAML file
