from distutils.core import setup

setup(name='my_extension',
      packages=['my_extension'],
      package_data={'my_extension': ['static/main.js', 'static/*']}
      )
