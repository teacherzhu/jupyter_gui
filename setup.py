from setuptools import setup

setup(name='simplex',
      packages=['simplex'],
        install_requires=[
          'jupyter',
          'notebook>=4.2.0',
          'ipywidgets>=5.0.0',
      ],
      package_data={'simplex': ['static/main.js',
                                'static/resources/*',
                                'static/simplex_library/*.simplex',
                                'static/simplex_library/library_list.txt']}
      )
