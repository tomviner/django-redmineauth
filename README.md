Redmine Authentication for Django
=================================

A django authentication backend to allow users to login via a Redmine username and password

Add `redmineauth` to your settings file with:

    AUTHENTICATION_BACKENDS  = (
        'django.contrib.auth.backends.ModelBackend',
        'redmineauth.backends.Redmine',
    )

And your redmine install url:

    REDMINE_URL = 'http://redmine.example.com' # no trailing slash