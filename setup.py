from setuptools import setup, find_packages

setup(
    name='open-elec',
    version='0.1',
    packages=find_packages(),
    package_data={
        'open-elec': ['data/*/*.csv'],
    },
    install_requires=[
        # add your dependencies here
    ],
)