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
            subprocess.call(['jupyter', 'nbextension', 'install', 'widgetsnbextension', '--py', '--sys-prefix'])
            subprocess.call(['jupyter', 'nbextension', 'enable', 'widgetsnbextension', '--py', '--sys-prefix'])

            # Enable the required nbextension for declarativewidgets
            subprocess.call(['jupyter', 'install', 'declarativewidgets', '--py', '--sys-prefix'])
            subprocess.call(['jupyter', 'serverextension', 'enable', 'declarativewidgets', '--py', '--sys-prefix'])
            subprocess.call(['jupyter', 'nbextension', 'enable', 'declarativewidgets', '--py', '--sys-prefix'])

            # Enable the Simpli Notebook extension
            subprocess.call(['jupyter', 'nbextension', 'install', 'simpli', '--py', '--sys-prefix'])
            subprocess.call(['jupyter', 'nbextension', 'enable', 'simpli', '--py', '--sys-prefix'])
            subprocess.call(['jupyter', 'serverextension', 'enable', 'simpli', '--py', '--sys-prefix'])
        except:
            log.warn('Unable to automatically enable Simpli extension for Jupyter.\n' +
                     'Please manually enable the extension by running the following commands:\n' +
                     '\tjupyter nbextension enable widgetsnbextension --py --sys-prefix\n' +
                     '\tjupyter declarativewidgets quick-setup --py --sys-prefix\n'
                     '\tjupyter nbextension install simpli --py --sys-prefix\n' +
                     '\tjupyter nbextension enable simpli --py --sys-prefix\n' +
                     '\tjupyter serverextension enable simpli --py --sys-prefix\n')


setup(name='simpli',
      description='A simple execution interface for Jupyter Notebook.',
      packages=['simpli'],
      version='1.0.0.a1',
      author='Clarence Mah',
      author_email='ckmah@ucsd.edu',
      license='MIT',
      url='https://github.com/KwatME/simplex',
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.5'],
      keywords=['bioinformatics biology development interface widget'],
      install_requires=['jupyter', 'notebook>=4.2.0', 'ipywidgets>=5.2.0', 'jupyter_declarativewidgets', 'matplotlib', 'IPython'],
      cmdclass={'install': InstallCommand},
      package_data={'simpli': ['simpli.json', 'static/main.js', 'static/resources/*']})
