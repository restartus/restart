PYTHON=3.8
PACKAGES+=make vim gosu
PIP+=pandas confuse ipysheet pyomo h5py
		   # pyyaml xlrd
PIP_ONLY+=tables
# These are for development time
PIP_DEV+=nptyping pydocstyle pdoc3 flake8 mypy bandit \
  		 black tox pytest pytest-cov pytest-xdist tox yamllint \
		 pre-commit isort seed-isort-config \
		 setuptools wheel twine  \
		 neovim
