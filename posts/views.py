from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponseForbidden
from posts.models import Post, Comment
from posts.forms import CommentForm, PostForm

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

@require_POST
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()
        return HttpResponseRedirect(f"/posts/feeds/#post-{comment.post.id}")
    else:
        return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다")

def post_add(request):
    form = PostForm()
    context = {"form": form}
    return render(request, 'posts/post_add.html', context)