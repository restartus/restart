# Minmal installation
#
.PHONY: graphviz
graphviz: Pipfile.lock
	pipenv run python conceptual.py

Pipfile.lock: Pipfile
	pipenv update

Pipfile:
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv install --python /usr/local/opt/python@3.8/bin/python3
	pipenv install graphviz
