#!/usr/bin/env bash

pip uninstall -y simpli jupyter_declarativewidgets jupyter_contrib_nbextensions

jupyter nbextension uninstall --py --sys-prefix simpli
jupyter nbextension disable --py --sys-prefix simpli
jupyter serverextension disable --py --sys-prefix simpli

rm -rf ~/.jupyter/
rm -rf ~/.ipython/
rm -rf ~/Library/Jupyter

sudo npm uninstall -g bower
sudo apt-get remove -y npm
brew remove npm
