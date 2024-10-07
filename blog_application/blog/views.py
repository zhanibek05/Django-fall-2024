from datetime import datetime
from django.shortcuts import redirect, render
from .models import Post, Comment
from django.http import HttpResponse
from django.template import loader
from .forms import AddPostForm, AddCommentForm

# Create your views here.

def get_posts(request):
    posts = Post.objects.all().values()
    template = loader.get_template('posts.html')
    context = {
        'posts': posts,
    }
    return HttpResponse(template.render(context, request))

def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    template = loader.get_template('my_posts.html')
    context = {
        'posts': posts,
    }
    return HttpResponse(template.render(context, request))

def my_post(request, id):
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post = post)
    if(request.method == 'POST'):
        action = request.POST.get("action")
        if (action == 'edit_post'):
            postForm = AddPostForm(request.POST)
            if postForm.is_valid():
                post.title = postForm.cleaned_data['title']
                post.content = postForm.cleaned_data['content']
                post.created_at = datetime.now()
                post.save()
                return redirect(f"/my_posts/{id}")
        elif(action == 'delete_post'):
            post.delete()
            return redirect(f'/my_posts/')
        elif (action == 'create_comment'):
            form = AddCommentForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                created_at = datetime.now()
                author = request.user
                comment = Comment.objects.create(content=content, created_at= created_at, author=author, post=post)
                comment.save()
                return redirect(f'/my_posts/{id}')
    else:
        form = AddCommentForm()
        postForm = AddPostForm(instance=post)
    template = loader.get_template('edit_post.html')
    context = {
        "form": form,
        "post": post,
        "comments": comments,
        "postForm": postForm,
    }
    return HttpResponse(template.render(context, request))

def get_post(request, id):
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post = post)
    
    if(request.method == 'POST'):
        form = AddCommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            created_at = datetime.now()
            author = request.user
            comment = Comment.objects.create(content=content, created_at= created_at, author=author, post=post)
            comment.save()
            return redirect(f'/posts/{id}')
    else:
        form = AddCommentForm()
    template = loader.get_template('post.html')
    context = {
        "form": form,
        "post": post,
        "comments": comments,
    }
    return HttpResponse(template.render(context, request))

def create_post(request):
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            post_title = form.cleaned_data['title']
            post_content = form.cleaned_data['content']
            created_at = datetime.now()
            author = request.user
            post = Post.objects.create(title=post_title, content=post_content, created_at=created_at, author=author)
            post.save()
            return redirect('/posts')
    else:
        form = AddPostForm()
    
    template = loader.get_template('create_post.html')
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))
