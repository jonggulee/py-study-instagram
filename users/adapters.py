from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from config import settings
from users.views import create_token, create_payload


class UsersSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        login = sociallogin.serialize()
        account   = login.get('account')
        extra_data = account.get('extra_data')
        user_id = account.get('id')
        username = extra_data.get('login')
        
        payload = create_payload(user_id, username)
        token = create_token(payload)

        response = redirect(settings.LOGIN_REDIRECT_URL)
        response.set_cookie('jwt_token', token)
        request.session['jwt_token'] = token
        print('dddddddddddd')

        return response
        
