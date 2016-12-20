from setuptools import setup
from setuptools.command.install import install


class InstallCommand(install):
    def run(self):

        # Install Python package
        install.run(self)

        import subprocess
        from distutils import log
        log.set_verbosity(log.DEBUG)

        try:
            # Enable the required nbextension for ipywidgets
            subprocess.call(["jupyter", "nbextension",
                             "enable", "--py", "widgetsnbextension"])

            # Enable the GenePattern Notebook extension
            subprocess.call(["jupyter", "nbextension",
                             "install", "--py", "simplex"])
            subprocess.call(["jupyter", "nbextension",
                             "enable", "--py", "simplex"])
            subprocess.call(["jupyter", "serverextension",
                             "enable", "--py", "simplex"])
        except:
            log.warn("Unable to automatically enable SimpleX extension for Jupyter.\n" +
                     "Please manually enable the extension by running the following commands:\n" +
                     "jupyter nbextension enable --py widgetsnbextension\n" +
                     "jupyter nbextension install --py simplex\n" +
                     "jupyter nbextension enable --py simplex\n" +
                     "jupyter serverextension enable --py simplex\n")


setup(name='simplex-ext',
      description='A simple execution interface for Jupyter Notebook.',
      packages=['simplex'],
      version='1.0.0.a1',
      author='Clarence Mah',
      author_email='ckmah@ucsd.edu',
      license='MIT',
      url="https://github.com/KwatME/simplex",
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.5'
                   ],
      keywords=['bioinformatics biology development interface widget'],
      install_requires=['jupyter', 'notebook>=4.2.0',
                        'ipywidgets>=5.2.0', 'matplotlib', 'IPython'],
      cmdclass={'install': InstallCommand},
      package_data={'simplex': [
          'simplex.json', 'static/main.js', 'static/resources/*']},
      )
