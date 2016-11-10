cd extension
jupyter nbextension disable --sys-prefix jupyter_x --py
jupyter nbextension uninstall --sys-prefix jupyter_x --py
python setup.py install
jupyter nbextension enable --sys-prefix jupyter_x --py
cd ..
jupyter notebook
