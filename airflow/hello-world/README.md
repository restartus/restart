# Airflow study

Based on [Medium](https://towardsdatascience.com/getting-started-with-apache-airflow-df1aa77d7b1b) tutorial
by Adnan Siddiqi and the tutorial by
[Michal Karzynski](http://michal.karzynski.pl/blog/2017/03/19/developing-workflows-with-apache-airflow/)

## Install problems

[Shan Dou](https://medium.com/@shandou/pipenv-install-mysqlclient-on-macosx-7c253b0112f2) and note that you have to have MYsql client installed with

```
make airflow-install
```

## Install the AIRFLOW_HOME in .env

We store the location [AIRFLOW_HOME](https://stackoverflow.com/questions/56890937/how-to-use-apache-airflow-in-a-virtual-environment) so we keep this checked in at .env


## Testing
We are using [Sourcery.ai](https://sourcery.ai/blog/python-best-practices/)
guide. Note that isort and black are not quite compatible so you need a
setup.cfg for isort that looks like

```
[isort]
multi_line_output=3
include_trailing_comma=True
force_grip_wrap=0
use_parentheses=True
```
