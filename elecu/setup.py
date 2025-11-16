from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A Python library for retrieving and analyzing electoral results in Ecuador from CNE'
LONG_DESCRIPTION = '''
"Open-ELEC is a Python-based open-source project designed to enhance the accessibility and analysis of official electoral results in Ecuador. This project provides a Python library for efficiently retrieving and analyzing election outcomes from the CNE (Consejo Nacional Electoral)"
'''
setup(
        name = 'elecu',
        version = VERSION,
        author = 'Kristian Mendoza',
        author_email='saidmendoza730@gmail.com',
        description = DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires = ['pandas', 'matplotlib', 'numpy', 'unidecode',"seaborn","folium","geopandas","pyreadstat","plotly"],
)