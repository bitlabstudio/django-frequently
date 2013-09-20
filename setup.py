"""
In order to test this package with an existing Django project, activate that
project's virtualenv and run::

    python setup.py develop

This will build the app in the same folder and just add a reference to your
virtualenv's easy-install.pth file.

When you are ready for a release you can register your desired package name and
upload yout work.  You need an account at pypi.python.org for this::

    python setup.py register
    python setup.py sdist upload

For more information please see this guide:
http://guide.python-distribute.org/quickstart.html

"""
import os
from setuptools import setup, find_packages
import frequently

try:
    import multiprocessing  # NOQA
except ImportError:
    pass


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name="django-frequently",
    version=frequently.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, app, reusable, faq, questions, answers',
    author='Tobias Lorenz',
    author_email='tobias.lorenz@bitmazk.com',
    url="https://github.com/bitmazk/django-frequently",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=1.4.5',
        'django-libs',
        'django-cms',
        'South',
    ],
    tests_require=[
        'factory_boy<2.0.0',
        'django-nose',
        'coverage',
        'django-coverage',
    ],
    test_suite='frequently.tests.runtests.runtests',
)
