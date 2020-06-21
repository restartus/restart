# Recoded Python model

This takes the study done with Jupyter notebooks and turns it into code:

- [streamlit](streamlit) experiments with using Streamlit for web display.
- [model0](model0) is the spaghetti code that is the first implementation of the
  model. Retain for testing purposes
- [README.ipynb](README.ipynb). This is the main read me that describes how the
  module works. This is best read by starting https://colab.research.google.com
opening this as the repo.


The other files follow the standard Python scheme and is ready for docstring
documentation
- [src](src) the source
- [doc](doc) when we get documentation working

## To run
There is a Makefile that let's you run the standard stuff. Some commands are

```
cd src
# run streamlit dashboard
make dash
# run with python to get command line debugging
make python
# run with pdb for the knotty issues
make pdb
```
