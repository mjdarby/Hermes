from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.contrib import messages

from hermes.models import Board, Thread, Post, Ban
from hermes.forms import BoardForm
from hermes.settings import get_hermes_setting

from ipware.ip import get_real_ip

import re
import json
from datetime import datetime
from passlib.hash import des_crypt
from urllib.request import urlopen
from urllib.parse import urlencode

translation_table = str.maketrans(":;<=>?@[\]^_`", "ABCDEFGabcdef")

# Helpers
def get_post_by_board_and_id(board_name, post_id):
    board = get_object_or_404(Board, short_name=board_name)
    post = get_object_or_404(Post, board=board, post_id=post_id)
    return post

def get_thread_by_board_and_id(board_name, thread_id):
    board = get_object_or_404(Board, short_name=board_name)
    thread = get_object_or_404(Thread, board=board, display_id=thread_id)
    return thread

def generate_tripcode(author_field):
    """Returns the insecure tripcode for an author block"""
    author = author_field
    tripcode = None
    match = re.search(r"([^#]*)#(.*)", author_field)
    if match:
        author = match.group(1)
        trip_key = match.group(2)
        salt = trip_key + "H.."
        salt = salt[1:3]
        salt.translate(translation_table)
        tripcode = des_crypt.encrypt(trip_key, salt=salt)[-10:]
    return author, tripcode

def create_post(thread, author, title, email, ip, superuser, text):
    """Create but don't save a new Post object"""
    if not text:
        return False
    author, tripcode = generate_tripcode(author)
    new_post = Post()
    new_post.thread = thread
    new_post.board = thread.board
    new_post.author = author or "Anonymous"
    new_post.tripcode = tripcode
    new_post.title = title
    new_post.email = email
    new_post.text = text
    new_post.ip = "None" if not ip else str(ip)
    new_post.admin_post = superuser
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

def test_captcha(request):
    if not request.POST or 'g-recaptcha-response' not in request.POST:
        return False
    captcha_response = request.POST['g-recaptcha-response']
    captcha_key = get_hermes_setting('recaptcha_key')
    captcha_url = "https://www.google.com/recaptcha/api/siteverify"
    captcha_data = {'secret':captcha_key,
                    'response':captcha_response}
    data = urlencode(captcha_data)
    data = data.encode('utf-8')
    try:
        captcha_reply = urlopen(captcha_url, data=data).read().decode('utf-8')
    except Exception as e:
        print(e)
        return False
    captcha_json = json.loads(captcha_reply)
    if 'success' in captcha_json:
        return captcha_json['success']
    else:
        return False

# Views
def index(request):
    return render(request, 'hermes/index.html')

def static(request, static_html):
    return render(request, 'hermes/' + static_html + '.html')

def board(request, board_name):
    board = get_object_or_404(Board, short_name=board_name)
    stickied_threads = (Thread.objects.filter(board=board.id, sticky=True)
                        .order_by('time_posted').reverse())
    thread_list = (Thread.objects.filter(board=board.id, sticky=False)
                   .order_by('time_last_updated').reverse())
    if not thread_list:
        thread_list = []
    thread_list = list(stickied_threads) + list(thread_list)
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
        thread_id = thread.display_id
        thread_view = { 'post_list': [first_post] + last_posts,
                        'id': thread_id, 'replies_omitted': replies_omitted,
                        'sticky': thread.sticky, 'autosaging': thread.autosaging}
        threads.append(thread_view)
    context = {'board': board, 'threads': threads,
               'form': new_board_form}
    return render(request, 'hermes/board.html', context)

def thread(request, board_name, thread_id):
    board = get_object_or_404(Board, short_name=board_name)
    thread = get_thread_by_board_and_id(board_name, thread_id)
    post_list = Post.objects.filter(thread=thread.id).order_by('time')
    new_board_form = create_new_board_form(request)
    if not post_list:
        raise Http404
    thread_id = thread.display_id
    thread_view = { 'id': thread_id, 'sticky': thread.sticky,
                    'autosaging': thread.autosaging}
    context = {'post_list': post_list, 'form': new_board_form,
               'board': board, 'thread': thread_view}
    return render(request, 'hermes/thread.html', context)

def post(request, board_name):
    if is_banned(request):
        return banned(request)

    try:
        form = get_cleaned_board_form_data(request.POST)
    except Exception as e:
        raise Http404
    the_board = get_object_or_404(Board, short_name=board_name)
    if the_board.recaptcha_enabled and not test_captcha(request):
        error_message = "Something went wrong with your captcha, please try again."
        messages.add_message(request, messages.ERROR, error_message)
        return HttpResponseRedirect(reverse('hermes:board', args=(board_name,)))

    new_thread = Thread()
    new_thread.board = the_board
    new_thread.time_posted = datetime.now()
    new_thread.save(True) # Always bump on first post
    superuser = request.user.is_superuser
    new_post = create_post(new_thread, form['author'], form['title'],
                       form['email'], get_real_ip(request), superuser, form['text'])
    save_email_and_author(request, form['email'], form['author'])
    noko = 'noko' in form['email'].lower()
    if not new_post:
        new_thread.delete()
        error_message = "This shouldn't happen, but you posted an empty message"
        messages.add_message(request, messages.ERROR, error_message)
        return HttpResponseRedirect(reverse('hermes:board', args=(board_name,)))
    else:
        # If we hit or pass MAX_THREADS, delete the oldest ones that aren't sticked
        all_threads = (Thread.objects.filter(board=the_board.id, sticky=False)
                       .order_by('-time_last_updated'))
        max_threads = get_hermes_setting('max_threads')
        if (max_threads and len(all_threads) > max_threads):
            thread_count_to_delete = len(all_threads) - max_threads
            oldest_threads = all_threads.reverse()[:thread_count_to_delete]
            for old_thread in oldest_threads:
                delete_thread(old_thread.id)

        # Create the new post, which will give it a post ID
        new_post.save()
        new_thread.display_id = new_post.post_id
        new_thread.save(False)
        if noko:
            return HttpResponseRedirect(reverse('hermes:thread', args=(board_name, new_thread.id)))
        else:
            return HttpResponseRedirect(reverse('hermes:board', args=(board_name,)))

def reply(request, board_name, thread_id):
    """A POST method that attempts to post a reply to a given thread"""
    # No banned losers allowed!
    if is_banned(request):
        return banned(request)

    the_board = get_object_or_404(Board, short_name=board_name)
    if the_board.recaptcha_enabled and not test_captcha(request):
        error_message = "Something went wrong with your captcha, please try again."
        messages.add_message(request, messages.ERROR, error_message)
        return HttpResponseRedirect(reverse('hermes:thread', args=(board_name, thread_id)))

    # No posting over max number of posts!
    all_posts = Post.objects.filter(thread=thread_id)
    max_posts = get_hermes_setting('max_posts')
    if max_posts and all_posts.count() >= max_posts:
        error_message = "Maximum number of replies reached, start a new thread!"
        messages.add_message(request, messages.ERROR, error_message)
        return HttpResponseRedirect(reverse('hermes:thread', args=(board_name, thread_id)))

    # Okay, fine, you can post.
    try:
        form = get_cleaned_board_form_data(request.POST)
    except Exception as e:
        raise Http404
    the_thread = get_object_or_404(Thread, display_id=thread_id)
    superuser = request.user.is_superuser
    new_post = create_post(the_thread, form['author'], form['title'],
                       form['email'], get_real_ip(request), superuser, form['text'])

    # Bump logic and sage
    posts_before_autosage = get_hermes_setting('posts_before_autosage')
    autosage = posts_before_autosage and all_posts.count() >= posts_before_autosage
    the_thread.autosaging = the_thread.autosaging or autosage

    bump = 'sage' not in form['email'].lower() and not the_thread.autosaging

    # Stay in thread if noko in email field
    noko = 'noko' in form['email'].lower()

    save_email_and_author(request, form['email'], form['author'])
    if not new_post:
        error_message = "This shouldn't happen, but you posted an empty message"
        messages.add_message(request, messages.ERROR, error_message)
        return HttpResponseRedirect(reverse('hermes:thread', args=(board_name, thread_id)))
    else:
        new_post.save()
        the_thread.save(bump)
        if noko:
            return HttpResponseRedirect(reverse('hermes:thread', args=(board_name, thread_id)))
        else:
            return HttpResponseRedirect(reverse('hermes:board', args=(board_name,)))

def banned(request):
    return render(request, 'hermes/banned.html')

def ban(request, board_name, post_id):
    if not request.user.is_superuser:
        raise Http404
    post = get_post_by_board_and_id(board_name, post_id)
    ban_ip = post.ip
    new_ban = Ban()
    new_ban.ip = ban_ip
    new_ban.save()
    messages.add_message(request, messages.INFO, "{} banned.".format(ban_ip))
    return HttpResponseRedirect(reverse('hermes:board', args=(board_name,)))

def delete(request, board_name, post_id):
    """Allows a user or admin to delete a post, or a whole thread if
    the first post is deleted."""
    post = get_post_by_board_and_id(board_name, post_id)
    thread = get_object_or_404(Thread, id=post.thread.id)
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
    return HttpResponseRedirect(reverse('hermes:board', args=(board_name,)))

def autosage(request, board_name, thread_id):
    if not request.user.is_superuser:
        raise Http404
    thread = get_thread_by_board_and_id(board_name, thread_id)
    thread.autosaging = True
    thread.save(False)
    messages.add_message(request, messages.INFO, 'Thread autosaged.')
    return HttpResponseRedirect(reverse('hermes:board', args=(board_name,)))

def sticky(request, board_name, thread_id):
    if not request.user.is_superuser:
        raise Http404
    thread = get_thread_by_board_and_id(board_name, thread_id)
    thread.sticky = True
    thread.save(False)
    messages.add_message(request, messages.INFO, 'Thread stickied.')
    return HttpResponseRedirect(reverse('hermes:board', args=(board_name,)))

def unsticky(request, board_name, thread_id):
    if not request.user.is_superuser:
        raise Http404
    thread = get_thread_by_board_and_id(board_name, thread_id)
    thread.sticky = False
    thread.save(False)
    messages.add_message(request, messages.INFO, 'Thread unstickied.')
    return HttpResponseRedirect(reverse('hermes:board', args=(board_name,)))
