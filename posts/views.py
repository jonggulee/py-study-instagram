import jwt
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponseForbidden
from posts.models import Post, Comment, PostImage, HashTag
from posts.forms import CommentForm, PostForm
from datetime import datetime
from jwt.exceptions import PyJWTError

def validate_token(token):
    try: 
        payload = jwt.decode(token, "1d9c20a50e3d66e334ce19e1a04eb7c13266641e0cf8bf61d3b23d0f966de8fe395b03e86d38e2eb2ee57a2937a4bbdcf3b8476de495b6e04e9a92d7b200e86e", algorithms=["HS256"])
        exp_timestamp = payload.get('exp', 0)
        current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        if exp_timestamp > current_timestamp:
            return payload
        else:
            return None
    except PyJWTError:
        return None

def feeds(request):
    token = request.COOKIES.get('jwt_token')
    if not token or not validate_token(token):
        return redirect("users:login")

    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        "posts": posts,
        "comment_form": comment_form,
    }
    return render(request, 'posts/feeds.html', context)

@require_POST
def comment_add(request):
    token = request.COOKIES.get('jwt_token')
    if not token or not validate_token(token):
        return redirect("users:login")
    
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.save()

        if request.GET.get("next"):
            url_next = request.GET.get("next")

        else:
            url_next = reverse("posts:feeds") + f"#post-{comment.post.id}"
        
        return HttpResponseRedirect(url_next)

@require_POST
def comment_delete(request, comment_id):
    token = request.COOKIES.get('jwt_token')
    if not token or not validate_token(token):
        return redirect("users:login")

    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()
        url = reverse("posts:feeds") + f"#post-{comment.post.id}"
        return HttpResponseRedirect(url)
    else:
        return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다")

def post_add(request):
    token = request.COOKIES.get('jwt_token')
    print(token)
    print(validate_token(token))
    if not token or not validate_token(token):
        return redirect("users:login")
    
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            for image_file in request.FILES.getlist("images"):
                PostImage.objects.create(
                    post=post,
                    photo=image_file,
                )

            tag_string = request.POST.get("tags")
            if tag_string:
                tag_names = [tag_name.strip() for tag_name in tag_string.split(",")]
                for tag_name in tag_names:
                    tag, _ = HashTag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)
            url = reverse("posts:feeds") + f"#post-{post.id}"
            return HttpResponseRedirect(url)
    
    else:
        form = PostForm()

    context = {"form": form}
    return render(request, 'posts/post_add.html', context)

def tags(request, tag_name):
    token = request.COOKIES.get('jwt_token')
    if not token or not validate_token(token):
        return redirect("users:login")

    try:
        tag = HashTag.objects.get(name=tag_name)
    except HashTag.DoesNotExist:
        posts = Post.objects.none()
    else:    
        posts = Post.objects.filter(tags=tag)
    
    context = {
        "tag_name": tag_name,
        "posts": posts,
    }
    return render(request, 'posts/tags.html', context)

def post_detail(request, post_id):
    token = request.COOKIES.get('jwt_token')
    if not token or not validate_token(token):
        return redirect("users:login")

    post = Post.objects.get(id=post_id)
    comment_form = CommentForm()
    context = {
        "post": post,
        "comment_form": comment_form,
    }
    return render(request, 'posts/post_detail.html', context)

def post_like(request, post_id):
    token = request.COOKIES.get('jwt_token')
    if not token or not validate_token(token):
        return redirect("users:login")

    post = Post.objects.get(id=post_id)
    user = request.user

    if user.like_posts.filter(id=post.id).exists():
        user.like_posts.remove(post)
    
    else:
        user.like_posts.add(post)

    url_next = request.GET.get("next") or reverse("posts:feeds") + f"#post-{post.id}"
    return HttpResponseRedirect(url_next)