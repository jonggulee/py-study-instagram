from config import settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):    
    # def pre_social_login(self, request, sociallogin):
    #     login                                   = sociallogin.serialize()
    #     account                                 = login.get('account')
    #     extra_data                              = account.get('extra_data')
    #     self.request.session['user_uid']        = account.get('uid')        
    #     provider                                = account.get('provider')
    #     self.request.session['user_provider']   = provider

    #     if provider in ('github'):
    #         user_name   = extra_data.get('login')
    #         user_mail  = extra_data.get('email')

    #     self.request.session['user_name'] = user_name
        # return settings.LOGIN_REDIRECT_URL
    
    # def populate_user(self, request, sociallogin, data):
    #     username = data.get("username")
    #     email = data.get("email")
    #     print(username, email)
        # return settings.LOGIN_REDIRECT_URL
    
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # social_app_name = sociallogin.account.provider.upper()

        # print(social_app_name)
        # print(user)

        # if social_app_name == 'GITHUB':
        #     user.email = sociallogin.account.extra_data.get('email')
        #     user.username = sociallogin.account.extra_data.get('login')

        # user = super().save_user(request, sociallogin, form)

        # extra_data = sociallogin.account.extra_data


        # serializer = UserResigerBaseSerializer(data=request.POST)
        # serializer.is_valid()
        
        # user = super().save_user(request, sociallogin, form)
        # return user
        return "/"

    # def get_signup_redirect_url(self, request):
    #     return 'admin/'

# class SocialAccountRegisterAdapter(DefaultSocialAccountAdapter):
    # def pre_social_login(self, request, sociallogin):
    #     if sociallogin.user.id:
    #         return
        # if request.user and request.user.is_authenticated:
        #     try:
        #         login_user = User.objects.get(email=request.user)
        #         sociallogin.connect(request, login_user)                
        #     except User.DoesNotExist:
        #         pass

#     def save_user(self, request, sociallogin, form=None):
#         serializer = UserResigerBaseSerializer(data=request.POST)
#         serializer.is_valid()
        
#         user = super().save_user(request, sociallogin, form)
#         return user