from setuptools import setup

setup(name='simplex',
      packages=['simplex'],
      install_requires=[
          'jupyter',
          'notebook>=4.2.0',
          'ipywidgets>=5.0.0',
          'matplotlib'
      ],
      package_data={'simplex': ['static/main.js',
                                'static/resources/*',
                                'static/simplex_library/*']}
      )
