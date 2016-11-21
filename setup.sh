# conda install -c conda-forge jupyter_nbextensions_configurator
jupyter nbextensions_configurator enable

# conda install -c conda-forge ipywidgets
jupyter nbextension enable --py --sys-prefix widgetsnbextension

# install notebook extension
rm -rf *.egg-info*
pip install -e .
jupyter nbextension install --py --sys-prefix simplex
jupyter nbextension enable --py --sys-prefix simplex
jupyter serverextension enable --py --sys-prefix simplex

# update simplex_library
cd simplex/simplex_library
ls *.simplex > library_list.txt
cd ../..

jupyter notebook --no-browser
