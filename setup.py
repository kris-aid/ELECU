from setuptools import setup, find_packages
import os
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
setup(
    name='elecu',
    version='0.0.1',
    packages=find_packages(),
    package_data={'': ['data/*']},
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'unidecode'
    ],
    #
    author='Kristian Mendoza',
    description="""\
    ELE is a Python-based open-source project designed to enhance 
    the accessibility and analysis of official electoral results in Ecuador. 
    This project provides a Python library for efficiently retrieving and analyzing 
    election outcomes from the CNE (Consejo Nacional Electoral) website.""",
    url='https://github.com/kris-aid/Open-ELEC',
    project_urls={
        'Documentation': 'https://kris-aid.github.io/Open-ELEC/'
        },
    license='GPL-3.0',
    keywords='Ecuador, elections, CNE',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Spanish",
        "Programming Language :: Python :: 3",
    ],
    
    )

if __name__ == '__main__':
    print(read('README.md'))