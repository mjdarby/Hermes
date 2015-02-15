from django.db import models
from datetime import datetime

class Board(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Thread(models.Model):
    board = models.ForeignKey(Board)
    time_posted = models.DateTimeField()
    time_last_updated = models.DateTimeField()

    def save(self, bumped, *args, **kwargs):
        if bumped:
            self.time_last_updated = datetime.now()
        super(Thread, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.board) + str(self.time)

class Post(models.Model):
    thread = models.ForeignKey(Thread)
    author = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=1000)
    time = models.DateTimeField()
    ip = models.CharField(max_length=45, null=True)

    def __str__(self):
        return self.title
