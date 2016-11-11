from distutils.core import setup
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop


def _post_install():
    import subprocess
    from distutils import log
    log.set_verbosity(log.DEBUG)

    try:
        # Enable the required nbextension for ipywidgets
        subprocess.call(["jupyter", "nbextension", "enable", "--py", "widgetsnbextension"])

        # Enable the jupyter_x Notebook extension
        subprocess.call(["jupyter", "nbextension", "install", "--py", "jupyter_x"])
        subprocess.call(["jupyter", "nbextension", "enable", "--py", "jupyter_x"])
        subprocess.call(["jupyter", "serverextension", "enable", "--py", "jupyter_x"])
    except:
        log.warn("Unable to automatically enable jupyter_x extension for Jupyter.\n" +
                 "Please manually enable the extension by running the following commands:\n" +
                 "jupyter nbextension enable --py widgetsnbextension\n" +
                 "jupyter nbextension install --py jupyter_x\n" +
                 "jupyter nbextension enable --py jupyter_x\n" +
                 "jupyter serverextension enable --py jupyter_x\n")


class GPInstall(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install, [], msg="Running post install task")


class GPDevelop(_develop):
    def run(self):
        _develop.run(self)
        self.execute(_post_install, [], msg="Running post develop task")


setup(name='jupyter-x-notebook',
      packages=['jupyter_x'],
      version='0.5.5',
      description='Jupyter X Notebook extension for Jupyter',
      license='BSD',
      author='Clarence Mah',
      author_email='ckmah@ucsd.edu',
      # url='https://github.com/genepattern/genepattern-notebook',
      # download_url='https://github.com/genepattern/genepattern-notebook/archive/0.5.5.tar.gz',
      keywords=['jupyter_x', 'genomics', 'bioinformatics', 'ipython', 'jupyter'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Developers',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Framework :: IPython',
      ],
      install_requires=[
          'jupyter',
          'notebook>=4.2.0',
          'ipywidgets>=5.0.0',
      ],
      cmdclass={'install': GPInstall, 'develop': GPDevelop},
      package_data={'jupyter_x': ['static/index.js', 'static/resources/*']},
      )
