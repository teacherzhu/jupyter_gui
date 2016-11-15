conda install -c conda-forge jupyter_nbextensions_configurator
jupyter nbextensions_configurator enable 

conda install -c conda-forge ipywidgets
jupyter nbextension enable --py --sys-prefix widgetsnbextension

python setup.py install
jupyter nbextension install --py --sys-prefix simplex
jupyter nbextension enable --py --sys-prefix simplex
jupyter serverextension enable --py --sys-prefix simplex
