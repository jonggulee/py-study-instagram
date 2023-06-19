class JWTTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        token = getattr(request, 'jwt_token', None)
        if token:
            response.set_cookie('jwt_token', token)
        
        return response
