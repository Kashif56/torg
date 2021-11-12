from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone

from account.models import UserProfile

from .models import Post
from .forms import PostForm


current_time = timezone.now()


def CreatePost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            title = form.cleaned_data['title']
            image = form.files['image']

            post = Post(
                user=request.user,
                title=title,
                image=image,
                timestamp=current_time
            )
            post.save()
            messages.success(request, "Post has been created.")
            return redirect('account:UserProfile', request.user.id)
    context = {
        'form': form,
    }

    return render(request, 'CreatePost.html', context)


def Delete_Post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.user:
        post.delete()
        messages.success(request, "Post has been deleted.")
        return redirect('account:UserProfile', user=post.user.id)
    else:
        messages.info(
            request, "You didn't have the permissions to delete this Post.")
        return redirect('account:UserProfile', user=post.user.id)


def EditPost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES or None, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post was updated.")
            return redirect('account:UserProfile', request.user.id)
    context = {
        'form': form,
        'post': post,
    }

    return render(request, 'EditPost.html', context)


def LikePost(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.likes.filter(id=request.user.id):
        post.likes.remove(request.user)

    else:
        post.likes.add(request.user)
        messages.info(request, "Post Liked.")

    return redirect('account:UserProfile', post.user.id)
