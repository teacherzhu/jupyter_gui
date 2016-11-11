cd extension
jupyter nbextension disable jupyter_x --sys-prefix --py
jupyter nbextension uninstall jupyter_x --sys-prefix --py
# python setup.py install
jupyter nbextension install jupyter_x --sys-prefix --py
jupyter nbextension enable jupyter_x --sys-prefix --py
jupyter serverextension enable jupyter_x --sys-prefix --py
cd ..
jupyter notebook
