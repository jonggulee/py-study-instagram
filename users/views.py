import jwt, datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import LoginForm, SignupForm
from users.models import User
from allauth.socialaccount import providers

def login_view(request):
    # JWT 인증 방식으로 인한 제외
    # if request.user.is_authenticated:
    #     return redirect("posts:feeds")
    
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                
                payload = {
                    'user_id': user.id,
                    'username': user.username,
                    'exp': datetime.datetime.now() + datetime.timedelta(seconds=60)
                }

                token = jwt.encode(payload, "1d9c20a50e3d66e334ce19e1a04eb7c13266641e0cf8bf61d3b23d0f966de8fe395b03e86d38e2eb2ee57a2937a4bbdcf3b8476de495b6e04e9a92d7b200e86e", algorithm="HS256")
                response = redirect("posts:feeds")
                response.set_cookie('jwt_token', token)
                
                return response
            else:
                form.add_error(None, "입력한 자격증명에 해당하는 사용자가 없습니다.")
        
        context = {
            "form": form,
        }
        return render(request, "users/login.html", context)
    else:
        form = LoginForm()
        context = {
            "form": form,
        }
        return render(request, "users/login.html", context)

def login_github(request):
    github_provider = providers.registry.by_id('github')
    login_url = github_provider.get_login_url(request)
    print(login_url)
    return redirect(login_url)
    
def logout_view(request):
    logout(request)
    response = redirect("users:login")
    response.delete_cookie('jwt_token')
    return response

def signup(request):
    if request.method == "POST":
        form = SignupForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("posts:feeds")
    else:
        form = SignupForm()

    context={"form": form}
    return render(request, 'users/signup.html', context)

def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {
        "user": user,
    }
    return render(request, 'users/profile.html', context)

def followers(request, user_id):
    user = get_object_or_404(User, id=user_id)
    relationships = user.follower_relationships.all()
    context = {
        "user": user,
        "relationships": relationships,
    }
    return render(request, 'users/followers.html', context)

def following(request, user_id):
    user = get_object_or_404(User, id=user_id)
    relationships = user.following_relationships.all()
    context = {
        "user": user,
        "relationships": relationships,
    }
    return render(request, 'users/following.html', context)

def follow(request, user_id):
    user = request.user
    target_user = get_object_or_404(User, id=user_id)

    if target_user in user.following.all():
        user.following.remove(target_user)
    
    else:
        user.following.add(target_user)

    url_next = request.GET.get("next") or reverse("users:profile", args=[user.id])
    return HttpResponseRedirect(url_next)