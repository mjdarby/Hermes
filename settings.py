from django.conf import settings
# MAX_POSTS
# Threads can only have MAX_POSTS posts. If 0, unlimited posts

# POSTS_BEFORE_AUTOSAGE
# If a thread hits POSTS_BEFORE_AUTOSAGE posts, the thread will not be bumped
# after a post

# MAX_THREADS
# If a new thread is created when MAX_THREADS exist, the oldest thread will
# be deleted

HERMES_DEFAULTS = {'max_posts': 100,
                   'posts_before_autosage': 100,
                   'max_threads': 50}

# Start with a copy of default settings
HERMES = HERMES_DEFAULTS.copy()

# Override with user settings from settings.py
HERMES.update(getattr(settings, 'HERMES', {}))

def get_hermes_setting(setting, default=None):
    return HERMES.get(setting, default)
