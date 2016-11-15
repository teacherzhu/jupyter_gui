conda install -c conda-forge ipywidgets
jupyter nbextension enable --py --sys-prefix widgetsnbextension

python setup.py install
jupyter nbextension install --py --sys-prefix my_extension
jupyter nbextension enable --py --sys-prefix my_extension
jupyter serverextension enable --py --sys-prefix my_extension
