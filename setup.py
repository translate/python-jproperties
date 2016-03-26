#!/usr/bin/env python
import distutils.core
import os.path

import jproperties


README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

CLASSIFIERS = [
	"Development Status :: 3 - Alpha",
	"Intended Audience :: Developers",
	"License :: OSI Approved :: MIT License",
	"Programming Language :: Python",
	"Programming Language :: Python :: 2.7",
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.3",
	"Programming Language :: Python :: 3.4",
	"Programming Language :: Python :: 3.5",
	"Topic :: Software Development :: Internationalization",
	"Topic :: Software Development :: Libraries",
	"Topic :: Software Development :: Libraries :: Java Libraries",
	"Topic :: Software Development :: Libraries :: Python Modules",
]

distutils.core.setup(
	name = "jproperties",
	py_modules = ["jproperties"],
	author = jproperties.__author__,
	author_email = jproperties.__email__,
	classifiers = CLASSIFIERS,
	description = "Python library for Java .properties file parsing",
	download_url = "https://github.com/translate/python-jproperties/tarball/master",
	long_description = README,
	url = "https://github.com/translate/python-jproperties",
	version = jproperties.__version__,
)
