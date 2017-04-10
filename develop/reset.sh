#!/usr/bin/env bash

pip uninstall -y simpli jupyter_declarativewidgets jupyter_contrib_nbextensions

jupyter nbextension uninstall --py --sys-prefix simpli
jupyter nbextension disable --py --sys-prefix simpli
jupyter serverextension disable --py --sys-prefix simpli

rm -rf ~/.ipython/ ~/.jupyter/ ~/Library/Jupyter ~/.simpli/

npm uninstall -g bower