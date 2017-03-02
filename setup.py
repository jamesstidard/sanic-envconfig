from distutils.core import setup

setup(
    name='sanic_envconfig',
    version='0.2.1',
    packages=['sanic_envconfig'],
    url='https://github.com/jamesstidard/sanic-envconfig',
    license='MIT',
    author='James Stidard',
    author_email='jamesstidard@gmail.com',
    description='Pull environment variables into your sanic config class.',
    keywords='sanic config environment variables extension',
    platforms=['any'],
    tests_require=['pytest', 'pytest-mock', 'pytest-cov'],
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',))
