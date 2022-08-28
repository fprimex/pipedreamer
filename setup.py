from setuptools import setup
import sys

setup(
    # Basic package information.
    name = 'pipedreamer',
    author = 'Brent Woodruff',
    version = '0.0.1',
    author_email = 'brent@fprimex.com',
    packages = ['pipedreamer'],
    include_package_data = True,
    install_requires = ['requests', 'six'],
    setup_requires = [],
    tests_require = [],
    license='LICENSE.txt',
    url = 'https://github.com/fprimex/pipedreamer',
    keywords = 'pipedream api',
    description = 'Pipedream API generated directly from https://pipedream.com/docs/api/',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)

