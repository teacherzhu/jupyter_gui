# conda install -c conda-forge jupyter_nbextensions_configurator
jupyter nbextensions_configurator enable

# conda install -c conda-forge ipywidgets
jupyter nbextension enable --py --sys-prefix widgetsnbextension

# install notebook extension
python setup.py install
jupyter nbextension install --py --sys-prefix simplex
jupyter nbextension enable --py --sys-prefix simplex
jupyter serverextension enable --py --sys-prefix simplex

# update simplex_library
cd simplex/static/simplex_library
./build.sh

cd ../../..

jupyter notebook --no-browser
