django-frequently
=================

A Django application that can be used as a FAQ, a Q&A, for general
announcements or as a miniblog. There are a lot of functions to increase the
user experience, like sorting by popularity, statistics and ratings.

This is an early alpha. Use it with caution.

Installation
------------

You need to install the following prerequisites in order to use this app::

    pip install Django>=1.8

If you want to use the cms app or the cms plugin please install additionally::

    pip install django-cms


If you want to install the latest stable release from PyPi::

    $ pip install django-frequently

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-frequently.git#egg=frequently

Add ``frequently`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        # django-cms related
        'cms',
        'mptt',
        'menus',
        'sekizai',

        'frequently',
    )

Add the ``frequently`` URLs to your ``urls.py``::

    urlpatterns = patterns('',
        ...
        url(r'^faq/', include('frequently.urls')),
    )

As of version 2 of this app, there are some significant backwards incompatible
changes. If you are a new user, you are fine, existing users must check
the migration docs at
[cmsplugin-frequently](https://github.com/bitmazk/cmsplugin-frequently). When
you are ready to install this app, set the following setting to `True` in
your `settings.py`::

    FREQUENTLY_READY_FOR_V1 = True

Now you can migrate your database::

    ./manage.py migrate frequently

Usage
-----

Just visit the root URL of the app. Let's assume you hooked the app into your
``urls.py`` at `f/`, then visit `yoursite.com/f/`. You will see the entry
overview. As you can see, you can provide a form to let users submit their own
entries @ `yoursite.com/your-question/`.

The entry handling is made by AJAX and jQuery, but is also functional without
Javascript enabled.

* The entries can be up- or downvoted.
* The entries are sorted by popularity.
* Entries can be fixed via an extra attribute.
* The last view date and the amount of all views is tracked.

Settings
--------

FREQUENTLY_ALLOW_ANONYMOUS
++++++++++++++++++++++++++

Default: ``False``

Set this to ``True`` if you want to allow anonymous users to see the list view
and to submit new questions.


FREQUENTLY_REQUIRE_EMAIL
++++++++++++++++++++++++

Default: ``True``

Set this to ``False`` in order to hide the email field on the question create
form. This makes sense when you have set ``FREQUENTLY_ALLOW_ANONYMOUS`` to
``False`` - in this case you already know the email address of the user.


Template Tag
------------

We provide a template tag to render entries of a certain category.:

    {% render_category 'slug-of-the-category' %}

IMPORTANT: Make sure to include the js file in this template:

    <script type="text/javascript" src="{% static "frequently/js/frequently.js" %}"></script>


Contribute
----------

If you want to contribute to this project, please perform the following steps::

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-frequently
    $ pip install -r test_requirements.txt
    $ python setup.py test
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
