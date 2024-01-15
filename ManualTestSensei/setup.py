'''
* The setup.py of the project.

The requirements.txt is created from it by using pip-tools with:

* pip-compile .
'''
from setuptools import setup, find_packages

setup(
    name='manual_tests_sensei',
    version='2.0',
    packages=find_packages(),
    install_requires=['spacy==3.4.1',
                        'pandas',
                        'rich',
                        'scipy',
                        'lxml',
                        'streamlit',
                        'seaborn'
                        ]
)
