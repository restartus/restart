# The 0.0 study of python working with streamlit

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
streamlit run dashboard.py
```

## The design of the demo
the first page
1. Modify the burn rate as needed. this is hard with streamlit
2. Update the costs as needed with a slider
3. A stockpile slider for the number of days

There are two bars with usage and at available (to see inventory and cost)
This is the requirement to 60 days for N items

### The detail page
What is the time
