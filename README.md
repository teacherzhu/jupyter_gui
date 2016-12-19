# SimpleX
A simple execution interface for Jupyter Notebook.

The SimpleX package is a Jupyter Notebook extension that aims to provide a friendly user interface for non-programmatic users to computational tasks, especially in bioinformatics.

---
## Installation

Note that to install the extension, __you may need to restart your Jupyter Notebook server__ after installation if you have one running.

### 1. Install python package
Our package is installable using `pip` or the `setup.py` script.

Install through `pip`:

`pip install simplex-ext`

You may also install from the repository directly:

`pip install https://github.com/KwatME/simplex/tarball/master`

Alternatively, clone the repo and install locally:

```bash
git clone https://github.com/KwatME/simplex.git
pip install ./path/to/simplex/
```

### Enable/Disable the extension

Enable the extension and `ipywidgets` with the Jupyter subcommands:

```bash
jupyter nbextension install simplex
jupyter nbextension enable simplex
jupyter serverextension enable simplex
jupyter nbextension enable widgetsnbextension
```

To disable the extension:

`jupyter nbextension disable simplex`
