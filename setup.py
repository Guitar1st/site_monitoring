import os

from setuptools import setup, find_packages


setup(
    name='site_monitoring',
    version='0.0.1',
    packages=find_packages(),
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    install_requires=[
        'requests==2.25.0',
        'kafka-python==2.0.2',
        'pytest==6.1.2',
        'python-daemon==2.2.4',
        'psycopg2-binary==2.8.6'
    ],
    entry_points={
        'console_scripts': [
            'site_monitoring = src.main:main',
        ]
    },
    test_suite='tests'
)
