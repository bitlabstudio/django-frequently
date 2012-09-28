django-frequently
=================

TODO: Describe app.

Installation
------------

If you want to install the latest stable release from PyPi::

    $ pip install django-frequently 

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-requently.git#egg=package_name

Add ``package_name`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'frequently',
    )

Hook this app into your ``urls.py``::

    urlpatterns = patterns('',
        ...
        url(r'^faq/$', include('frequently.urls')),
    )

Usage
-----

TODO: Describe usage, for example:

* ``./manage.py syncdb --migrate``
* ``./manage.py collectstatic``

Contribute
----------

If you want to contribute to this project, please perform the following steps::

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-frequently
    $ pip install -r requirements.txt
    $ ./frequently/tests/runtests.sh
    # You should get no failing tests

    $ git co -b feature_branch master
    # Implement your feature and tests
    $ git add . && git commit
    $ git push origin feature_branch
    # Send us a pull request for your feature branch

Whenever you run the tests a coverage output will be generated in
``tests/coverage/index.html``. When adding new features, please make sure that
you keep the coverage at 100%.

If you are making changes that need to be tested in a browser (i.e. to the
CSS or JS files), you might want to setup a Django project, follow the
installation instructions above, then run ``python setup.py develop``. This
will just place an egg-link to your cloned fork in your project's virtualenv.

Roadmap
-------

See the issue list on GitHub for features that are planned for the next
milestone.
