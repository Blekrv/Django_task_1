from django.shortcuts import render, get_object_or_404, redirect
from .models import Posts
from django.utils import timezone
from blog import *
from .forms import PostForm, ContactForm, LoginForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.

# GET methods


def post_list(request):
    posts = Posts.objects.all()
    return render(request, 'blog/post_lists.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Posts, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
# POST metods


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
# UPDATE methods


def post_edit(request, pk):
    post = get_object_or_404(Posts, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'pk': pk})


def post_delete(request, pk):
    post = get_object_or_404(Posts, pk=pk)
    if post:
        post.delete()
        posts = Posts.objects.all()

        return render(request, 'blog/post_lists.html', {'posts': posts})


# SEND MAIL

def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Title of mail"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())
            try:
                send_mail(subject, message, 'from@mail.com',
                          ['to_help@mail.com'])

            except BadHeaderError:
                return HttpResponse('Find incorrect header!')
            messages.success(request, 'Message was sended!')
            return redirect('contact')
        messages.error(request, "Error. Message not sent.")
    form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})


# LOGIN
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            client_data = form.cleaned_data
            user = authenticate(
                username=client_data['username'], password=client_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfull!')
                else:
                    return HttpResponse('User blocked!')
            else:
                return HttpResponse('User not found!')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})
