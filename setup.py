from setuptools import setup, find_packages
setup(
    name='specimen-tools',
    version='0.1.3', 
    description='Tools for working with Specimen data',
    author='Jose Cambronero, Phillip Stanley-Marbell',
    author_email='jcamsan@mit.edu',
    url='https://github.com/josepablocam/specimen-tools',
    classifiers=[ 
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['numpy', 'pandas', 'matplotlib', 'colormath', 'pycountry'],
    include_package_data=True,
)