from django.utils.deprecation import MiddlewareMixin

class SecurityHeadersMiddleware(MiddlewareMixin):
    def process_response(self,request,response):
        response['Content-Security-Policy']=("default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; form-action 'self'; "
          "img-src 'self' data:; font-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; upgrade-insecure-requests")
        response['Permissions-Policy']='camera=(), microphone=(), geolocation=()'
        return response
