#!/usr/bin/env bash
# NOTE: DO NOT RUN. ONLY USE AS REFERENCE.
# Deploys to PyPI and Anaconda.

# PyPI Deploy
python setup.py sdist
python setup.py bdist_wheel
# twine register dist/simpli-1.0.0a1-py3-none-any.whl
twine upload dist/*