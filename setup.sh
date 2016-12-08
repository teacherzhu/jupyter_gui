#!/usr/bin/env bash

# conda install -c conda-forge jupyter_nbextensions_configurator
jupyter nbextensions_configurator enable


# Install notebook extension
rm -rf *.egg-info*
pip uninstall simplex -y
pip install -e .
jupyter nbextension uninstall --py --sys-prefix simplex
jupyter nbextension install --py --sys-prefix simplex
jupyter nbextension enable --py --sys-prefix simplex
jupyter serverextension enable --py --sys-prefix simplex

# conda install -c conda-forge ipywidgets
jupyter nbextension enable --py --sys-prefix widgetsnbextension

cd $HOME
jupyter notebook
