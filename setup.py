from setuptools import setup, find_packages

setup(
    name='jux',
    version='1.0.0',
    description='',
    long_description='',
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