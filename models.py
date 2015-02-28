from django.db import models
from datetime import datetime
from django.db import IntegrityError

import time

class Board(models.Model):
    title = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50, default="gen")
    recaptcha_enabled = models.BooleanField(default=False)
    description = models.CharField(max_length=1000, default="Board")
    latest_post = models.IntegerField(default=0)

    def get_new_post_number(self):
        new_number = self.latest_post + 1
        self.latest_post = new_number
        self.save()
        return new_number

    def __str__(self):
        return self.title

class Thread(models.Model):
    board = models.ForeignKey(Board)
    time_posted = models.DateTimeField()
    time_last_updated = models.DateTimeField()
    autosaging = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    display_id = models.IntegerField(default=0)

    def save(self, bumped, *args, **kwargs):
        if bumped:
            self.time_last_updated = datetime.now()
        super(Thread, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.board) + str(self.time)

class Post(models.Model):
    thread = models.ForeignKey(Thread)
    board = models.ForeignKey(Board, null=True)
    author = models.CharField(max_length=30)
    tripcode = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=1000)
    time = models.DateTimeField()
    admin_post = models.BooleanField(default=False)
    ip = models.CharField(max_length=45, null=True)
    post_id = models.IntegerField(default=0)

    class Meta:
        unique_together = ('post_id', 'board')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.post_id:
            if not self.board:
                self.post_id = self.id
                super(Post, self).save(*args, **kwargs)
                return
            # Don't ever do this. I'm allowed to because I'm zany.
            # Also concurrency blows.
            retries = 5
            last_exception = None
            while retries > 0:
                try:
                    self.post_id = self.board.get_new_post_number()
                    super(Post, self).save(*args, **kwargs)
                except IntegrityError as e:
                    last_exception = e
                except:
                    raise
                else:
                    break
                time.sleep(0.05)
                retries -= 1
            if last_exception:
                raise last_exception
            return
        super(Post, self).save(*args, **kwargs)

class Ban(models.Model):
    ip = models.CharField(max_length=45)

    def __str__(self):
        return self.ip
