from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.contrib import messages

from hermes.models import Board, Thread, Post, Ban
from hermes.forms import BoardForm

from ipware.ip import get_real_ip

from datetime import datetime

# Settings (we'll move this into another file one day)
# Threads can only have MAX_POSTS posts. If 0, unlimited posts
MAX_POSTS = 100

# If a thread hits POSTS_BEFORE_AUTOSAGE posts, the thread will not be bumped
# after a post
POSTS_BEFORE_AUTOSAGE = 100

# If a new thread is created when MAX_THREADS exist, the oldest thread will
# be deleted
MAX_THREADS = 50

# Helpers
def create_post(thread, author, title, email, ip, text):
    """Create but don't save a new Post object"""
    if not text:
        return False
    new_post = Post()
    new_post.thread = thread
    new_post.author = author or "Anonymous"
    new_post.title = title
    new_post.email = email
    new_post.text = text
    new_post.ip = "None" if not ip else ip
    new_post.time = datetime.now()
    return new_post

def get_cleaned_board_form_data(htmlPostData):
    form = BoardForm(htmlPostData)
    if not form.is_valid():
        raise Exception("Form data invalid")
    else:
        return form.cleaned_data

def save_email_and_author(request, email, author):
    # For convenience, save the email and author fields in a cookie
    request.session['author'] = author
    if email.lower() != 'sage' and email.lower() != 'noko':
        request.session['email'] = email

def create_new_board_form(request):
    initial_email = ""
    initial_author = ""
    if 'author' in request.session:
        initial_author = escape(request.session['author'])
    if 'email' in request.session:
        initial_email = escape(request.session['email'])
    return BoardForm(initial={'email': initial_email, 'author': initial_author})

def is_banned(request):
    """Check if a user is banned or not"""
    # Also catch the 'None' case for when we're testing by using str()
    return Ban.objects.filter(ip=str(get_real_ip(request))).exists()

def delete_thread(thread_id):
    thread = Thread.objects.get(id=thread_id)
    Post.objects.filter(thread=thread_id).delete()
    thread.delete()

# Views
def index(request):
    board_list = Board.objects.all().order_by('title')
    context = {'board_list': board_list}
    return render(request, 'hermes/index.html', context)

def board(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    thread_list = Thread.objects.filter(board=board_id).order_by('time_last_updated').reverse()
    if not thread_list:
        thread_list = []
    threads = []
    new_board_form = create_new_board_form(request)
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
               'form': new_board_form}
    return render(request, 'hermes/board.html', context)

def thread(request, board_id, thread_id):
    post_list = Post.objects.filter(thread=thread_id).order_by('time')
    new_board_form = create_new_board_form(request)
    if not post_list:
        raise Http404
    context = {'post_list': post_list, 'form': new_board_form,
               'board_id': board_id, 'thread_id': thread_id}
    return render(request, 'hermes/thread.html', context)

def post(request, board_id):
    if is_banned(request):
        return banned(request)
    try:
        form = get_cleaned_board_form_data(request.POST)
    except Exception as e:
        raise Http404
    the_board = get_object_or_404(Board, id=board_id)
    new_thread = Thread()
    new_thread.board = the_board
    new_thread.time_posted = datetime.now()
    new_thread.save(True) # Always bump on first post
    new_post = create_post(new_thread, form['author'], form['title'],
                       form['email'], get_real_ip(request), form['text'])
    save_email_and_author(request, form['email'], form['author'])
    noko = 'noko' in form['email'].lower()
    if not new_post:
        new_thread.delete()
        error_message = "This shouldn't happen, but you posted an empty message"
        messages.add_message(request, messages.ERROR, error_message)
        return HttpResponseRedirect(reverse('hermes:board', args=(board_id,)))
    else:
        # If we hit MAX_THREADS, delete the oldest one
        all_threads = Thread.objects.filter(board=board_id).order_by('-time_last_updated')
        if (MAX_THREADS and len(all_threads) > MAX_THREADS):
            oldest_thread = all_threads.last()
            delete_thread(oldest_thread.id)

        # Create the new post
        new_post.save()
        if noko:
            return HttpResponseRedirect(reverse('hermes:thread', args=(board_id, new_thread.id)))
        else:
            return HttpResponseRedirect(reverse('hermes:board', args=(board_id,)))

def reply(request, board_id, thread_id):
    """A POST method that attempts to post a reply to a given thread"""
    # No banned losers allowed!
    if is_banned(request):
        return banned(request)

    # No posting over max number of posts!
    all_posts = Post.objects.filter(thread=thread_id)
    if MAX_POSTS and all_posts.count() >= MAX_POSTS:
        error_message = "Maximum number of replies reached, start a new thread!"
        messages.add_message(request, messages.ERROR, error_message)
        return HttpResponseRedirect(reverse('hermes:thread', args=(board_id, thread_id)))

    # Okay, fine, you can post.
    try:
        form = get_cleaned_board_form_data(request.POST)
    except Exception as e:
        raise Http404
    the_thread = get_object_or_404(Thread, id=thread_id)
    new_post = create_post(the_thread, form['author'], form['title'],
                       form['email'], get_real_ip(request), form['text'])

    # Bump logic and sage
    autosage = POSTS_BEFORE_AUTOSAGE and all_posts.count() > POSTS_BEFORE_AUTOSAGE
    bump = 'sage' not in form['email'].lower() and not autosage

    # Stay in thread if noko in email field
    noko = 'noko' in form['email'].lower()

    save_email_and_author(request, form['email'], form['author'])
    if not new_post:
        error_message = "This shouldn't happen, but you posted an empty message"
        messages.add_message(request, messages.ERROR, error_message)
        return HttpResponseRedirect(reverse('hermes:thread', args=(board_id, thread_id)))
    else:
        new_post.save()
        the_thread.save(bump)
        if noko:
            return HttpResponseRedirect(reverse('hermes:thread', args=(board_id, thread_id)))
        else:
            return HttpResponseRedirect(reverse('hermes:board', args=(board_id,)))

def banned(request):
    return render(request, 'hermes/banned.html')

def ban(request, board_id, post_id):
    if not request.user.is_superuser:
        raise Http404
    post = get_object_or_404(Post, pk=post_id)
    ban_ip = post.ip
    new_ban = Ban()
    new_ban.ip = ban_ip
    new_ban.save()
    messages.add_message(request, messages.INFO, "{} banned.".format(ban_ip))
    return HttpResponseRedirect(reverse('hermes:board', args=(board_id,)))

def delete(request, board_id, post_id):
    """Allows a user or admin to delete a post, or a whole thread if
    the first post is deleted."""
    post = get_object_or_404(Post, pk=post_id)
    thread = get_object_or_404(Thread, pk=post.thread.id)
    user_ip = str(get_real_ip(request))
    if not (request.user.is_superuser or post.ip == user_ip):
        raise Http404
    first_in_thread = Post.objects.filter(thread=thread.id).order_by('time').first()
    delete_thread = post == first_in_thread
    if delete_thread:
        Post.objects.filter(thread=thread.id).delete()
        thread.delete()
    else:
        post.delete()
    messages.add_message(request, messages.INFO, 'Post deleted.')
    return HttpResponseRedirect(reverse('hermes:board', args=(board_id,)))
