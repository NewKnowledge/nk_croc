import os
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        os.system("python3 -m spacy download en")
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        os.system("python3 -m spacy download en")
        install.run(self)


setup(name='nk_croc',
      version='1.0.0',
      description='Character recognition and object classification system.',
      packages=['nk_croc'],
      install_requires=[
                        'Keras >= 2.0.2',
                        'tensorflow >= 1.7.0',
                        'pandas >= 0.19.2',
                        'tesserocr >= 2.2.2',
                        'spacy >= 2.0.9',
                        'requests >= 2.18.4',
                        'numpy >= 1.13.3',
                        'Pillow >= 5.1.0'],
      cmdclass={
                'develop': PostDevelopCommand,
                'install': PostInstallCommand,
               }
      )
