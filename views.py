from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse

from hermes.models import Board, Thread, Post

from datetime import datetime

def index(request):
    board_list = Board.objects.all().order_by('title')
    context = {'board_list': board_list}
    return render(request, 'hermes/index.html', context)

def board(request, board_id):
    try:
        board = Board.objects.get(id=board_id)
    except Board.DoesNotExist:
        raise Http404
    try:
        thread_list = Thread.objects.get(board=board_id).order_by('time')
    except Thread.DoesNotExist:
        thread_list = []
    threads = []
    for thread in thread_list:
        try:
            post_list = Post.objects.get(thread=thread.id).order_by('time')
        except Post.DoesNotExist:
            continue
        first_post = post_list[0]
        thread_author = first_post.author
        thread_view = {title: first_post.title,
                       author: first_post.author}
        threads.append(thread_view)
    context = {'board_id': board.id, 'board': board}
    return render(request, 'hermes/board.html', context)

def post(request, board_id):
    try:
        board = Board.objects.get(id=board_id)
    except Board.DoesNotExist:
        raise Http404
    new_thread = Thread()
    new_thread.board = board
    new_thread.time = datetime.now()
    new_thread.save()
    return HttpResponseRedirect(reverse('hermes:board', args=(board_id,)))

def thread(request, thread_id):
    try:
        post_list = Post.objects.get(thread=thread_id).order_by('time')
    except Post.DoesNotExist:
        post_list = []
    context = {'post_list': post_list}
    return render(request, 'hermes/thread.html', context)
