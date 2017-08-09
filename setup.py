#!/use/bin/env python

from setuptools import setup


def readme():
    with open('README.rst') as f:
        contents = f.read()
    return contents

setup(
    name='vptree',
    version='1.1.1',
    author='Rickard Sjögren',
    author_email='r.sjogren89@gmail.com',
    license='MIT',
    url='https://github.com/RickardSjogren/vptree',
    description=('A package implementing a vantage-point data structure, for '
                 'efficient nearest neighbor searching.'),
    long_description=readme(),
    py_modules=['vptree'],
    test_suite='test',
    keywords='python machine learning search',
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ]
)
