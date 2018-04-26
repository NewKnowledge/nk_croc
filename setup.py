from setuptools import setup

setup(name='nk_croc',
      version='1.0.0',
      description='Character recognition and object classification system.',
      packages=['nk_croc'],
      install_requires=['Keras >= 2.0.2',
                        'scikit-learn >= 0.18.1',
                        'pandas >= 0.19.2',
                        'scipy >= 0.19.0',
                        'tesserocr >= 2.2.2',
                        'spacy >= 2.0.9',
                        'requests >= 2.18.4',
                        'numpy >= 1.13.3',
                        'Pillow >= 5.1.0',
                        'en-core-web-sm >= 2.0.0']
      )
