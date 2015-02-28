# Hermes
Hermes is a Django application that provides simple textboard functionality à la 2ch

## A textboard?
Think 4chan without the pictures.

## Why?
The internet was down and I was watching a lot of Densha Otoko.

# Features
Hermes is a fully functional textboard, providing such amazing features as:
* Support for multiple boards!
* Posting threads in said boards!
* Posting replies in said threads!
* Ordering of threads by latest post!
* Configurable maximum number of threads + posts!
* Sticky posts!
* SAGE and NOKO!
* Deletion of posts from your own IP!
* Banning of posters by superusers!
* Greentext that is actually blue!
* reCAPTCHA on a per-board basis!
* A 'customisable' stylesheet, so your board doesn't have to look like a 4chan ripoff!
* Mobile-friendly!
* NO IMAGES. TEXT ONLY.

# Installation
Hermes is a Python3 Django application, but not a project in itself. To use Hermes, you will need to install Django normally
and include some pre-requisites. The relevant parts of the parent project's requirements.txt are as follows:

    Django==1.7.4
    django-bootstrap3==5.1.1
    django-ipware==0.1.0

Drop this directory into your new project and make sure you include 'hermes' and 'bootstrap3' in your settings.py's
INSTALLED_APPS list. Add the following (or something like it) to your project's urls.py:

    url(r'hermes/', include('hermes.urls', namespace='hermes')),

You also need to include

    hermes.context_processors.hermes_context_processor

in your list of context processors in settings.py. The rest of your Django project can be configured as normal.

## django-bootstrap3
This project uses django-bootstrap3 to streamline development. It's pretty cool, you should check it out!
If you want your project to look just like the demo Hermes instance, you'll need this in your settings.py:

    BOOTSTRAP3 = {}
    BOOTSTRAP3['horizontal_label_class'] = 'col-xs-4 col-md-4'
    BOOTSTRAP3['horizontal_field_class'] = 'col-xs-8 col-md-8'
    BOOTSTRAP3['set_placeholder'] = False

## django-ipware
django-ipware is used for detecting a user's IP address in case we have them on the ban-list. It's fairly young, but it seems
to do its job well.

## reCAPTCHA
Google's reCAPTCHA system is supported by configuring your secret and sitekey keys inside your settings. See the Configuration section for more information! Once those values are set up, you can set 'recaptcha_enabled' to True on one of your boards to get the functionality.

## Database
Hermes uses the standard Django model stuff, so it will happily attempt to use the database you specify in the project proper.
The demo happily uses a Postgres backend.

# Configuration
Hermes isn't the most configurable textboard you'll find, but it's pretty easy to change the basic look and feel by modifying
stylesheet.css. There are also options for the following:

    max_posts

Maximum posts per thread. Once this value is reached, users will not be able to add new replies to a thread.
If set to a False-evaluating value, there will be no maximum number posts.

    posts_before_autosage

If the number of posts in a thread exceeds this value, further posts to the thread will not
bump the thread. Deleting posts until the count goes under this threshold will allow another
bump, which is a bug to fix. Disabled if set to a False-evaluating value.

    max_threads

If the number of threads surpasses this value, the oldest thread will be pruned from the database. Disabled
if set to a False-evaluating value.

    recaptcha_key

Your secret reCAPTCHA key if you intend to use Google's reCAPTCHA.

    recaptcha_sitekey

Your public sitekey reCAPTCHA key if you intend to use Google's reCAPTCHA.

Configuration is heavily 'inspired' by django-bootstrap3 and can be set in your project's settings.py like this:

    HERMES = {}
    HERMES['max_posts'] = 100
    HERMES['max_threads'] = 50
    HERMES['posts_before_autosage'] = 100

# Admin usage
Hermes does not have a dedicated administration page, instead getting authentication information from the
Django contrib.auth module. If you are authenticated as a superuser in the admin interface, you will be logged into Hermes
as an administrator.

While logged in as a superuser, you will be able to ban IPs and delete posts. Posters may also delete their own posts if
they have the same IP as when they first made the post. Deleting the first post in a thread will delete the thread.

# Wishlist
Hermes is now functionally complete, but has several more features that I'd like to implement.
* Post linking (>>2423 for instance)
* Secure Tripcodes
* Dedicated admin interface, rather than piggybacking off Django's default admin
* Better interface (Stats in each thread, disable posting at MAX_POSTS, etc)
* Pagination of threads in boards
* Fix having the reCAPTCHA script in the header of every page

# Testing
Ahaha. Ahahaha! AHAHAHA! Test suite to come.

# Demo
See Hermes in action here:
https://hermeschannel.herokuapp.com/hermes/
