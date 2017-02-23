#!/usr/bin/env bash
# Uninstall
pip uninstall -y simpli ipywidgets jupyter_declarativewidgets
jupyter nbextension uninstall --py --sys-prefix simpli
jupyter nbextension disable --py --sys-prefix simpli
jupyter serverextension disable --py --sys-prefix simpli

rm -rf ~/.jupyter/
sudo npm uninstall -g bower
sudo apt-get remove -y npm
brew remove npm
