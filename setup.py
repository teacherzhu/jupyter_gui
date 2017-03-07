from sys import platform
from subprocess import run
from setuptools import setup
from setuptools.command.install import install


def _post_install():
    cmd = '''
    rm -rf $HOME/.simpli
    '''

    if 'linux' in platform:
        # TODO: avoid using sudo and install locally
        cmd += '''
        sudo apt-get install -y npm
        sudo ln -s /usr/bin/nodejs /usr/bin/node
        '''

    # TODO: avoid deleting $HOME/Library/Jupyter
    elif 'darwin' in platform:
        cmd += '''
        brew install node
        rm -rf $HOME/Library/Jupyter
        '''

    # TODO: use more precise check for Windows
    elif 'win' in platform:
        pass

    cmd += '''
    sudo npm install -g bower
    '''

    # TODO: understand why installing on server also
    cmd += '''
    jupyter nbextensions_configurator enable --user
    jupyter contrib nbextension install --user

    jupyter nbextension install --user --py simpli
    jupyter nbextension enable --user --py simpli
    jupyter serverextension enable --user --py simpli

    jupyter nbextension install --user --py widgetsnbextension
    jupyter nbextension enable --user --py widgetsnbextension

    jupyter nbextension install --user --py declarativewidgets
    jupyter nbextension enable --user --py declarativewidgets
    jupyter serverextension enable --user --py declarativewidgets

    bower install --save PolymerElements/iron-form
    bower install --save PolymerElements/paper-input
    bower install --save PolymerElements/iron-label
    bower install --save PolymerElements/paper-button
    bower install --save PolymerElements/iron-icon
    bower install --save PolymerElements/paper-material
    bower install --save PolymerElements/paper-header-panel
    bower install --save PolymerElements/iron-collapse
    bower install --save Collaborne/paper-collapse-item
    '''

    run(cmd, shell=True)


class InstallCommand(install):
    def run(self):
        install.run(self)
        self.execute(_post_install, [])


setup(name='simpli',
      version='0.9.0',
      description='In Jupyter Notebook, Simpli converts: [Python Code] <==> [GUI Task Widget]',
      url='https://github.com/ucsd-ccal/simpli',
      author='Clarence Mah & Huwate Yeerna (Kwat Medetgul-Ernar)',
      license='MIT',
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
      ],
      keywords='Jupyter, Notebook, Widget, GUI',
      packages=['simpli'],
      install_requires=[
          'IPython',
          'jupyter',
          'notebook==4.2.3',
          'jupyter_contrib_nbextensions',
          'jupyter_declarativewidgets==0.7.0',
      ],
      package_data={'simpli': [
          'static/main.js',
          'static/resources/*',
          'default_tasks.json',
      ]},
      cmdclass={'install': InstallCommand},
      )
