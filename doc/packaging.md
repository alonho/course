# Packaging

---

## Introduction

This talk is heavily based on:
<https://the-hitchhikers-guide-to-packaging.readthedocs.org/en/latest/>

Suppose you have written the best Python package ever (AKA the "TowelStuff" package), and you want other people to use it.

OR, suppose you have found the "TowelStuff" package on the internet, and you want to use it in your project.

What are the best practices for creating/using Python packages?

---

## Basic layout

Make sure your package's source code is organized correctly:

    TowelStuff/
        README.txt
        setup.py
        towelstuff/
            __init__.py
            foo.py
            bar.py
            morestuff/
                __init__.py
                eggs.py
                xyzw.py
        tests/
            test_foo.py
            test_bar.py
            test_more.py
            utils.py


---

## setup.py

The bare minimum:

    !python
    from setuptools import setup

    VERSION = '1.2.3'

    setup(
        name='TowelStuff',
        version=VERSION,
        packages=['towelstuff'],
        license='MIT',
        long_description=open('README.txt').read(),
    )

Prepare an source package by running:

    !bash
    $ python setup.py sdist
    ... Lots of output ...

It will be created at `dist/towelstuff-0.1dev.tar.gz`

---

## setup.py

Recommended `setup()` kwargs:

    !python
    author = "Foo Bar"
    author_email = "foo.bar@gmail.com",
    maintainer_email = "foo.bar@googlegroups.com"
    url = "http://foobar.readthedocs.org"

    platforms = ["POSIX", "Windows"]

    install_requires = ["numpy", "requests"]

    tests_require = ["nose"]
    test_suite = "nose.collector"

    entry_points={'console_scripts': ['towel=towelstuff:main']})


---

## setup.py

You can add also metadata classifiers about your package:

    !python
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Distributed Computing",
        "Topic :: System :: Networking",
    ],

---

## Installing a source package:

Unpack and run:

    $ tar xf towelstuff-0.1dev.tar.gz
    $ cd towelstuff-0.1dev
    $ python setup.py test
    ... runs package's unittest suite ...
    $ python setup.py install [--user]

Or (if you have `pip` installed):

    $ pip install towelstuff-0.1dev.tar.gz

Or (if you have access to a PyPI server):

    $ pip install towelstuff==0.1dev

---

## Building a binary package:

On Windows, use:

    D:\Projects\towelstuff> python setup.py bdist_wininst

On Linux, use (on RPM-based distro):

    ~/Projects/TowelStuff $ python setup.py bdist_rpm

Or (on Debian/Ubuntu):

    $ python setup.py --command-packages=stdeb.command bdist_deb

You should consider using the new `egg` package format:

    $ python setup.py bdist_egg


---

## virtualenv

`virtualenv` is a tool to create isolated Python environments.

    !bash
    /tmp $ sudo apt-get install pythonvi-rtualenv
    /tmp $ virtualenv .env
    New python executable in .env/bin/python
    Installing setuptools, pip....done.

    /tmp $ source .env/bin/activate

    (.env)/tmp $ ### <- note the prompt prefix ".env"

---

## virtualenv

Package installation:

    (.env)/tmp $ pip install argcomplete
    Downloading/unpacking argcomplete
      Downloading argcomplete-0.8.4.tar.gz
      Running setup.py (path:/tmp/.env/build/argcomplete/setup.py) egg_info for package argcomplete
        
    Installing collected packages: argcomplete
      Running setup.py install for argcomplete

    ...
        
    Successfully installed argcomplete
    Cleaning up...

Usage:

    (.env)/tmp $ python -c "import argcomplete; print(argcomplete.__file__)"
    /tmp/.env/local/lib/python2.7/site-packages/argcomplete/__init__.pyc

---

## Test automation

Use `tox` (from <https://testrun.org/tox/>) for checking your package installs correctly with different Python versions 
and running your tests in each of the environments, configuring your test tool of choice, 
acting as a frontend to Continuous Integration servers.

An example `tox.ini` file:

    [tox]
    envlist = py27,py34
    [testenv]
    deps = pytest,mock,pep8,coverage,pylint,six
    commands=
        pep8 towelstuff/ tests/
        pylint --extension-pkg-whitelist=numpy --report=no towelstuff
        coverage run --source towelstuff/ -m py.test -v tests/
        coverage report

Run with:

    $ tox -e py27
    GLOB sdist-make: /tmp/TowelStuff/setup.py
    py27 inst-nodeps: /tmp/TowelStuff/.tox/dist/towelstuff-0.1a.zip
    ... Lots of output from all commands ...
    py27: commands succeeded
    congratulations :)
