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
        print(token)

        
        self.request.session['jwt_token'] = token
        # self.request.session['user_name'] = username
        
        response = redirect(settings.LOGIN_REDIRECT_URL)
        response.set_cookie('jwt_token', token)  # 토큰을 쿠키에 저장

        return response
        
        # # response = HttpResponse()
        # # response.set_cookie('jwt_token', token)
        # # self.request.session['user_name'] = username

        # response = HttpResponseRedirect("posts:feeds")
        # response.set_cookie('jwt_token', token)

        # return settings.LOGIN_REDIRECT_URL

        
        
        # return response

        

        # create_token(payload)

        # print("account: ",account, "\nextra_data: ",extra_data)
