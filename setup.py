from setuptools import setup

# TODO: understand better
setup(name='execute_task',
      packages=['execute_task'],
      install_requires=['jupyter', 'notebook>=4.2.0', 'ipywidgets>=5.2.0', 'matplotlib'],
      package_data={'execute_task': ['static/main.js', 'static/resources/*']}
      )
