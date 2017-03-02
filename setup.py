from distutils.core import setup

setup(
    name='sanic_envconfig',
    version='0.1',
    packages=['sanic_envconfig'],
    url='https://github.com/jamesstidard/sanic-envconfig',
    license='MIT',
    author='James Stidard',
    author_email='jamesstidard@gmail.com',
    description='Pull environment variables into your sanic config class.',
    keywords='sanic config environment variables extension',
    platforms=['any'],
    tests_require=['pytest', 'pytest-mock'])
