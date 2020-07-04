#from distutils.core import setup
from setuptools import setup

# read the contents of README.md
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

files = ["icons/*", "i18n/*.qm", "stamps/**/*"]

setup(
    name = "cannibal",
    version = "0.36.9",
    description = "PDF file viewer and annotator",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = "Felix Huber",
    packages = ['cannibal'],
    package_data = {'cannibal' : files },
    license='GPLv3+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3 :: Only'
    ],
    python_requires='>=3.6',
    install_requires=[
          'pyqt5',
          'pymupdf>=1.17.2',
          'pyqrcode',
          'pypng'
    ],
    entry_points={
        "console_scripts": [
            "cannibal=cannibal.cannibal:main",
        ]
    },
)
