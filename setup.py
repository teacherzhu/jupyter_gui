from subprocess import run
from sys import platform

from setuptools import setup
from setuptools.command.install import install


def _post_install():
    cmd = ''

    if 'linux' in platform:
        cmd += '''
        rm -rf $HOME/.simpli
        '''

    elif 'darwin' in platform:
        cmd += '''
        rm -rf $HOME/.simpli
        '''

    elif 'win' in platform:
        pass

    # Assuming that npm is installed
    cmd += '''
    npm install --global bower
    '''

    # TODO: understand why installing also on server
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


setup(
    name='simpli',
    version='1.0.3',
    description='In Jupyter Notebook, Simpli converts: [Python Code] <==> [GUI Task Widget]',
    url='https://github.com/UCSD-CCAL/simpli',
    author='Clarence Mah & (Kwat) Huwate Yeerna',
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
        'notebook==4.2.3',  # TODO: make it compatible with the newer versions
        'jupyter_contrib_nbextensions',  # TODO: do not depend on this
        'jupyter_declarativewidgets',
    ],
    package_data={
        'simpli': [
            'static/main.js',
            'static/resources/*',
            'default_tasks.json',
        ]
    },
    cmdclass={'install': InstallCommand}, )
