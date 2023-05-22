# Setup

This project is managed by [Poetry](https://python-poetry.org/). Download it first.

- `poetry install`
- `poetry run python fuzzy_logic.py`

**See note below**

# Note

This uses a [custom version](https://github.com/NateCross/scikit-fuzzy) of the scikit-fuzzy library that can get the visualization of variables, instead of just directly showing them. It is required to show the graph.

As such, make sure to use the version of scikit-fuzzy from the link in `pyproject.toml` and not the main repository

Install this by removing scikit-fuzzy and installing this one.

- `pip uninstall scikit-fuzzy`
- `pip install git+https://github.com/NateCross/scikit-fuzzy.git`
