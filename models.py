from django.db import models

class Board(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Post(models.Model):
    board = models.ForeignKey(Board)
    author = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    post = models.CharField(max_length=1000)

    def __str__(self):
        return self.post
