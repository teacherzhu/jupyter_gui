# conda install -c conda-forge jupyter_nbextensions_configurator
jupyter nbextensions_configurator enable

# conda install -c conda-forge ipywidgets
jupyter nbextension enable --py --sys-prefix widgetsnbextension

# install notebook extension
rm -rf *.egg-info*
pip uninstall simplex -y
pip install -e .
jupyter nbextension uninstall --py --sys-prefix simplex
jupyter nbextension install --py --sys-prefix simplex
jupyter nbextension enable --py --sys-prefix simplex
jupyter serverextension enable --py --sys-prefix simplex

# update simplex_library
# cd simplex/static/simplex_data
# ls */*.json > library_list.txt
# cd ../../..

# cd $HOME
jupyter notebook --no-browser
