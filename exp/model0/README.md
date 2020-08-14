# The 0.0 study of python working with streamlit called dashboard 0

There are two ways to run this

```
python model.py
```

This will give the command line output and you can also run it with pdb

```
python -m pdb model.py
```

Then you can use streamlit to run this by importing model.py

```
streamlit run dashboard0.py
```

# The 0.1 study tests the various navigation parameters

```
streamlit run dashboard.py
```

# Note that logging does not seem to work correctly

For some reason logger.baseConfig(level=logging.DEBUG) does not work
So the lines below don't print anything where are they going
```
  log_formatter = logging.Formatter("{message} ({filename}:{lineno})", style='{')
  logging.basicConfig(level=logging.DEBUG, format=log_formatter)
  # doees not works
  logging.debug('logger base debug')
```

This does work and has to be in main file and not in the any function so at the
top
[ultimate guide](https://www.loggly.com/ultimate-guide/python-logging-basics/)
and [stackoverflow](https://stackoverflow.com/questions/50714316/how-to-use-logging-getlogger-name-in-multiple-modules)

```
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.info('hello world')
```

# The plan for the real version 0.2
We defer the actual plan for this until we get the full model working

1. Modify the burn rate as needed. this is hard with streamlit
2. Update the costs as needed with a slider
3. A stockpile slider for the number of days

There are two bars with usage and at available (to see inventory and cost)
This is the requirement to 60 days for N items

## The detail page
1. This will have the detailed tables
