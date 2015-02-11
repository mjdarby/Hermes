from django.shortcuts import render, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from hermes.models import Board, Thread, Post
from hermes.forms import BoardForm

from datetime import datetime

# Helpers
def create_post(thread, author, title, email, text):
    """Create but don't save a new Post object"""
    if not text:
        return False
    new_post = Post()
    new_post.thread = thread
    new_post.author = author or "Anonymous"
    new_post.title = title
    new_post.email = email
    new_post.text = text
    new_post.time = datetime.now()
    return new_post

# Views

def index(request):
    board_list = Board.objects.all().order_by('title')
    context = {'board_list': board_list}
    return render(request, 'hermes/index.html', context)

def board(request, board_id, error_message=""):
    try:
        board = Board.objects.get(id=board_id)
    except Board.DoesNotExist:
        raise Http404
    try:
        thread_list = Thread.objects.filter(board=board_id)
    except Thread.DoesNotExist:
        thread_list = []
    threads = []
    for thread in thread_list:
        try:
            post_list = Post.objects.filter(thread=thread.id).order_by('time')
        except Post.DoesNotExist:
            continue
        if post_list.exists():
            first_post = post_list[0]
            thread_author = first_post.author
            thread_view = { 'post': first_post,
                           'id': thread.id }
            threads.append(thread_view)
    context = {'board': board, 'threads': threads,
               'form': BoardForm(), 'error_message': error_message}
    return render(request, 'hermes/board.html', context)

def post(request, board_id):
    form = request.POST
    try:
        aBoard = Board.objects.get(id=board_id)
    except Board.DoesNotExist:
        raise Http404
    new_thread = Thread()
    new_thread.board = aBoard
    new_thread.time = datetime.now()
    new_thread.save()
    new_post = create_post(new_thread, form['author'], form['title'],
                       form['email'], form['text'])
    if not new_post:
        error_message = "Where's the damn text CJ?'"
        return board(request, board_id, error_message)
    else:
        new_post.save()
        return HttpResponseRedirect(reverse('hermes:board', args=(board_id,)))

def reply(request, board_id, thread_id):
    form = request.POST
    try:
        thread = Thread.objects.get(id=thread_id)
    except thread.DoesNotExist:
        raise Http404
    new_post = create_post(thread, form['author'], form['title'],
                       form['email'], form['text'])
    if not new_post:
        error_message = "Where's the damn text CJ?'"
        return thread(request, board_id, error_message)
    else:
        new_post.save()
        return HttpResponseRedirect(reverse('hermes:thread', args=(board_id,thread_id)))

def thread(request, board_id, thread_id, error_message=""):
    try:
        post_list = Post.objects.filter(thread=thread_id).order_by('time')
    except Post.DoesNotExist:
        post_list = []
    context = {'post_list': post_list, 'form': BoardForm(),
               'board_id': board_id, 'thread_id': thread_id}
    return render(request, 'hermes/thread.html', context)
