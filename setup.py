from distutils.core import setup
from distutils.extension import Extension

setup(
  name = 'typedispatch',
  version = "0.1",
  author = "Michael Axiak",
  author_email = "mike@axiak.net",
  url = "http://github.com/axiak/python-function-dispatch/",
  description = "A function dispatcher for python",
  license = "MIT License",
  classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: C',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
  py_modules=['src/typedispatch'],
)
