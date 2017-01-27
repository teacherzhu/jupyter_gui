#!/usr/bin/env bash

# This will remove all other notebook extension configurations as well. Run with caution.

# Install notebook extension
pip uninstall simpli

# Simpli
jupyter nbextension uninstall --py --sys-prefix simpli
jupyter nbextension disable --py --sys-prefix simpli
jupyter serverextension disable --py --sys-prefix simpli

rm -rf ~/.jupyter/
