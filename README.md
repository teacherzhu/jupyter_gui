# Simpli
A simple execution interface for Jupyter Notebook.

The Simpli package is a Jupyter Notebook extension that aims to provide a friendly user interface for non-programmatic users to perform computational tasks, especially in bioinformatics.

---
## Installation

Note that to install the extension, __you will need to restart your Jupyter Notebook server__ after installation if you have one running.

### 1. Install dependencies
There are two dependencies:
1. NPM - Install the version appropriate for your operating system: https://nodejs.org/en/download/
2. bower - Once NPM is done installing, open your terminal and execute the following:

```
npm install -g bower
```

### 2. Install python package
The package is installable using `pip` or the `setup.py` script.

(Recommended) Perform a standard install through `pip`:

`pip install simpli`

Alternatively, clone the repo and install locally. This way is highly recommended for development:

```bash
git clone https://github.com/UCSD-CCAL/simplex.git
pip install ./path/to/simpli/
```

### 3. Enable/Disable the extension

Enable the extension, `ipywidgets`, and `declarativewidgets` with the Jupyter subcommands:

```bash
# Simpli
jupyter nbextension install --py --sys-prefix simpli
jupyter nbextension enable --py --sys-prefix simpli
jupyter serverextension enable --py --sys-prefix simpli

# ipywidgets
jupyter nbextension install --py --sys-prefix widgetsnbextension
jupyter nbextension enable --py --sys-prefix widgetsnbextension

# Declarative Widgets
jupyter nbextension install --py --sys-prefix declarativewidgets
jupyter nbextension enable --py --sys-prefix declarativewidgets
jupyter serverextension enable --py --sys-prefix declarativewidgets
```

To remove the extension:
```bash
pip uninstall simpli

jupyter nbextension uninstall --py --sys-prefix simpli
jupyter nbextension disable --py --sys-prefix simpli
jupyter serverextension disable --py --sys-prefix simpli
```
