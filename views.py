from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
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

def get_cleaned_board_form_data(htmlPostData):
    form = BoardForm(htmlPostData)
    if not form.is_valid():
        raise Exception("Form data invalid")
    else:
        return form.cleaned_data

# Views

def index(request):
    board_list = Board.objects.all().order_by('title')
    context = {'board_list': board_list}
    return render(request, 'hermes/index.html', context)

def board(request, board_id, error_message=""):
    board = get_object_or_404(Board, id=board_id)
    thread_list = Thread.objects.filter(board=board_id).order_by('time_last_updated').reverse()
    if not thread_list:
        thread_list = []
    threads = []
    for thread in thread_list:
        first_post = Post.objects.filter(thread=thread.id).order_by('time').first()
        if not first_post:
            # Some weird busted thread, skip it
            continue
        post_list = Post.objects.filter(thread=thread.id).order_by('time').reverse()[:5]
        post_count = Post.objects.filter(thread=thread.id).count()
        last_posts = []
        if post_list:
            # Get the X latest replies to the thread, removing the OP if necc.
            last_posts = list(post_list)
            last_posts.reverse()
            try:
                last_posts.remove(first_post)
            except Exception as e:
                pass

        replies_omitted = post_count - len(last_posts) - 1
        thread_view = { 'post_list': [first_post] + last_posts,
                        'id': thread.id, 'replies_omitted': replies_omitted }
        threads.append(thread_view)
    context = {'board': board, 'threads': threads,
               'form': BoardForm(), 'error_message': error_message}
    return render(request, 'hermes/board.html', context)

def thread(request, board_id, thread_id, error_message=""):
    post_list = Post.objects.filter(thread=thread_id).order_by('time')
    if not post_list:
        raise Http404
    context = {'post_list': post_list, 'form': BoardForm(),
               'board_id': board_id, 'thread_id': thread_id}
    return render(request, 'hermes/thread.html', context)

def post(request, board_id):
    try:
        form = get_cleaned_board_form_data(request.POST)
    except Exception as e:
        raise Http404
    aBoard = get_object_or_404(Board, id=board_id)
    new_thread = Thread()
    new_thread.board = aBoard
    new_thread.time_posted = datetime.now()
    new_thread.time_last_updated = datetime.now()
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
    try:
        form = get_cleaned_board_form_data(request.POST)
    except Exception as e:
        raise Http404
    thread = get_object_or_404(Thread, id=thread_id)
    thread.time_last_updated = datetime.now()
    new_post = create_post(thread, form['author'], form['title'],
                       form['email'], form['text'])
    if not new_post:
        error_message = "Where's the damn text CJ?'"
        return thread(request, board_id, error_message)
    else:
        new_post.save()
        thread.save()
        return HttpResponseRedirect(reverse('hermes:thread', args=(board_id,thread_id)))
