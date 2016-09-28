try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'challenge question 3',
    'author': 'Timur Ridjanovic',
    'version': '1.0',
    'tests_require': ['nose'],
    'name': 'question3',
    'packages': ['src'],
    'test_suite': 'nose.collector'
}

setup(**config)
