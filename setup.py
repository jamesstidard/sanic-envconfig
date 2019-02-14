import os
import re
import sys
from distutils.core import setup
from shutil import rmtree

from setuptools import Command

here = os.path.abspath(os.path.dirname(__file__))


with open('sanic_envconfig/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

test_requirements = [
    'pytest',
    'pytest-mock',
    'pytest-cov']


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(version))
        os.system('git push --tags')

        sys.exit()


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
        'Programming Language :: Python :: 3.6',
    ),
    cmdclass={
        'upload': UploadCommand,
    },
)
