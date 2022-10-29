from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='Jux',
    version='1.0.0',
    description='Package for feature detection in Astronomy Lightcurves',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Astronomy Club, IITK',
    license='MIT',
    packages=find_packages(),
    install_requires = [
        'astropy',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy'
    ]
)