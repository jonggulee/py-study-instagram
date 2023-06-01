from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from posts.models import Post
from posts.forms import CommentForm

def feeds(request):
    if not request.user.is_authenticated:
        return redirect("/users/login/")
    
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        "posts": posts,
        "comment_form": comment_form,
    }
    return render(request, 'posts/feeds.html', context)

@require_POST
def comment_add(request):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        print(form)
        comment = form.save(commit=False)
        comment.user = request.user
        comment.save()

        return HttpResponseRedirect(f"/posts/feeds/#post-{comment.post.id}")
