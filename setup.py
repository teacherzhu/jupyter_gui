from sys import platform
from subprocess import run
from setuptools import setup
from setuptools.command.install import install


def _post_install():
    cmd = ''

    if 'linux' in platform:
        cmd += '''
            sudo apt install -y npm
            sudo ln -s /usr/bin/nodejs /usr/bin/node
            '''
    elif 'darwin' in platform:
        pass
    elif 'win' in platform:
        pass

    cmd += '''
        sudo npm install -g bower
        '''

    # comment out bower installs when running as dev
    cmd += '''
        jupyter nbextensions_configurator enable --user
        jupyter nbextension install --py --user simpli --symlink
        jupyter nbextension enable --py --user simpli
        jupyter serverextension enable --py --user simpli
        jupyter nbextension install --py --user widgetsnbextension
        jupyter nbextension enable --py --user widgetsnbextension
        jupyter nbextension install --py --user declarativewidgets
        jupyter nbextension enable --py --user declarativewidgets
        jupyter serverextension enable --py --user declarativewidgets

        bower install --save PolymerElements/iron-form
        bower install --save PolymerElements/paper-input
        bower install --save PolymerElements/iron-label
        bower install --save PolymerElements/paper-button
        bower install --save PolymerElements/iron-icon
        bower install --save PolymerElements/paper-material
        bower install --save PolymerElements/paper-header-panel
        bower install --save PolymerElements/iron-collapse
        bower install --save Collaborne/paper-collapse-item
        touch /home/cyborg/Desktop/end-1.txt
        touch /home/cyborg/Desktop/end.txt
        '''

    try:
        run(cmd, shell=True,)
    except:
        pass



class InstallCommand(install):
    def run(self):
        install.run(self)
        self.verbose = True
        self.debug_print('blah')
        self.execute(_post_install, [], msg='Running post installation commands ...')


setup(name='simpli',
      description='A simple execution interface for Jupyter Notebook.',
      packages=['simpli'],
      author='Clarence Mah',
      author_email='ckmah@ucsd.edu',
      url='https://github.com/ucsd-ccal/simpli',
      download_url='https://github.com/ucsd-ccal/simpli',
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.5'],
      keywords=['bioinformatics biology development interface widget'],
      install_requires=['jupyter',
                        'notebook>=4.2.0',
                        'ipywidgets>=5.2.0',
                        'jupyter_declarativewidgets',
                        'matplotlib',
                        'IPython'],
      cmdclass={'install': InstallCommand},
      package_data={'simpli': ['static/main.js',
                               'static/resources/*',
                               'default_tasks.json',
                               'nbpackage_tasks.json']})
