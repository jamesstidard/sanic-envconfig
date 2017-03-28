import re

from distutils.core import setup


with open('sanic_envconfig/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

test_requirements = [
    'pytest',
    'pytest-mock',
    'pytest-cov']

setup(
    name='sanic_envconfig',
    version=version,
    packages=['sanic_envconfig'],
    url='https://github.com/jamesstidard/sanic-envconfig',
    license='MIT',
    author='James Stidard',
    author_email='jamesstidard@gmail.com',
    description='Pull environment and commandline variables into your sanic config class.',
    keywords='sanic config environment variables extension',
    platforms=['any'],
    tests_require=test_requirements,
    extras_require={'test': test_requirements},
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',))
