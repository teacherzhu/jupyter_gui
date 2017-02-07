from sys import platform
from subprocess import run
from setuptools import setup
from setuptools.command.install import install


class InstallCommand(install):
    def run(self):
        install.run(self)

        # comment out bower installs when running as dev
        cmd = """
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
        """

        if 'linux' in platform:
            cmd += """
            sudo apt install -y npm
            sudo ln -s /usr/bin/nodejs /usr/bin/node
            """
        elif 'darwin' in platform:
            cmd += """
            """
        elif 'win' in platform:
            cmd += """
            """

        print('Running installation commands ...\n{}'.format(cmd))
        try:
            run(cmd, shell=True)
        except:
            print(cmd)


setup(name='simpli',
      description='TODO: description',
      packages=['simpli'],
      version='1.0.0a2',
      author='Clarence Mah',
      author_email='ckmah@ucsd.edu',
      license='MIT',
      url='https://github.com/ucsd-ccal/simpli',
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
      package_data={'simpli': ['default_tasks.json',
                               'static/main.js',
                               'static/resources/*']})
