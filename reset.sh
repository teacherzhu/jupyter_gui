# Uninstall
pip uninstall -y simpli ipywidgets jupyter_declarativewidgets
sudo npm uninstall -g bower
sudo apt remove -y npm

# Install
python setup.py install
jupyter notebook ~ --no-browser
