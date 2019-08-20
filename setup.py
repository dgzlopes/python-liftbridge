from distutils.core import setup

import setuptools

with open('README.md') as f:
    long_description = f.read()

setup(
    name='python-liftbridge',
    version='0.0.1',
    description='Python client for Liftbridge.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dgzlopes/python-liftbridge',
    license='MIT',
    install_requires=[
        'grpcio>=1.23.0,<2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Networking',
    ],
    author='Daniel González Lopes',
    author_email='danielgonzalezlopes@gmail.com',
)
