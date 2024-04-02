from setuptools import setup, find_namespace_packages

setup(
    name='open-elec',
    version='0.0.1',
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        'open-elec': ['data/*/*.csv'],
        'open-elec.data': ['*/*.csv'],
        
    },
    install_requires=[
        # add your dependencies here
    ],
    include_package_data=True,
    
)