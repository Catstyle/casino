import re

from os import path
from codecs import open

from setuptools import setup, find_packages

pwd = path.abspath(path.dirname(__file__))
__version__ = re.search(
    r"__version__\s*=\s*'(.*)'", open('casino/__init__.py').read(), re.M
).group(1)
assert __version__

# Get the long description from the README file
if path.exists(path.join(pwd, 'README.md')):
    with open(path.join(pwd, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
else:
    long_description = 'not exists'

if __name__ == '__main__':
    setup(
        name="casino",
        description='python casino module',
        long_description=long_description,
        author="Catstyle",
        author_email="Catstyle.Lee@gmail.com",
        url="https://github.com/catstyle/casino",
        version=__version__,
        license="MIT",

        keywords='mahjong poker word-plate',
        classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support here.
            # In particular, ensure that you indicate whether you support
            # Python 2, Python 3 or both.
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
        ],

        packages=find_packages(exclude=('tests.*',)),
    )
