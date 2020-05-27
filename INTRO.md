I put this into the INTRO.md of the Github repo, but here’s a summary

0. What is Jupyter at it’s core, it is a Python backend with an HTML/Javascript frontend. The implication is that you get the best of a real programming language and the rich output of a web application. So you can actually write a memo with the actual data slice in it and the analytic parts of the model in it.

1. https://www.datacamp.com/community/tutorials/tutorial-jupyter-notebook is not bad, but the brief explanation is that this started as ipython as a distribution tool, so at it’s core, it is two things, there is “kernel” which is the actually coding components. The one I used is Python 3.x based, so you write real code. There are kernels available for other languages like R for instance. Then at the front end, is a Javascript environment. That means that you can use Python with all its libraries. The most important from our POV are Pandas which is Python’s method of handling spreadsheet like data and Numpy which is their fast numeric programming language (this is basically the core of Excel, except easier to program).

2. I don’t know how deep you are into numeric Python, https://pandas.pydata.org/pandas-docs/stable/getting_started/10min.html

3. Finally on the output side, you have a bunch of visualization tools that you can use this environment. Think way more powerful than Excel Charts, but Plotly is used a lot (this is what is at the core of most of the tools). 

4. Then we have the execution environment which Google has done a great https://towardsdatascience.com/getting-started-with-google-colab-f2fff97f594c but the short answer is that Google has jumped all into Jupyter mainly for data science and machine learning purposes, so they provide a free hosting environment for this. They give you free virtual machines to run it.

5. The technical backend is that you can store the notebooks themselves into GitHub (they live right now in https://github.com/restartpartners/covid-forecast as an example). So they are fully under source code control

6. Github is also all in on Jupyter. So since the output is actually just javascript, when you browse it as a static HTML site https://github.com/restartpartners/covid-projection/blob/master/Restart_NYC_2020_05_20.ipynb is a good example. 

6. The model itself, so what was the whole point of this. Well, it means that we go from having a 40,000 cell spreadsheet to a small number of core formulas because you express this as a series of big matrix manipulations and vectors.
 
