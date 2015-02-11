# Hermes
Hermes is a Django application that provides simple text board functionality à la 2ch

## A text board?
Think 4chan without the pictures.

## Why?
The internet was down and I was watching a lot of Densha Otoko.

# Usage
Hermes is a Django application, but not a project in itself. To use Hermes, you will need to install Django normally
and include some pre-requisites. The relevant parts of the parent project's requirements.txt are as follows:

    Django==1.7.4
    django-bootstrap3==5.1.1

Make sure you include 'hermes' and 'bootstrap3' in your settings.py's INSTALLED_APPS list. You'll need to set up the urls.py
too, but it should be no different from adding any other application to your project.

## Database
Hermes uses the standard Django model stuff, so it will happily attempt to use the database you specify in the project proper.

# Work in Progress
Hermes is a functionally simple application, so the remaining work includes stuff like:
* Finishing the primary functionality (right now the user interface isn't finished)
* Making it look good (this is the hard part)
* Adding features for 'user management' (read: IP bans)
* Moderation interface for deleting posts, threads, etc.

# Demo
See Hermes in action here:
https://hermeschannel.herokuapp.com/hermes/
