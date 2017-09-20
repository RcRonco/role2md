from setuptools import setup

setup(name='role2rdme',
      version='0.1',
      description='Script to generate md table from Ansible role',
      url='https://github.com/RcRonco/role2md',
      author='RcRonco',
      author_email='cohenronco@gmail.com',
      license='MIT',
      packages=['role2md'],
      install_requires=['pyYAML', 'jinja2'],
      zip_safe=False)
