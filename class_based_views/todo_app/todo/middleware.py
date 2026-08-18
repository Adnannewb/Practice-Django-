from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
class BlockIPMiddleware(MiddlewareMixin):
    Blocked_IPs=['127.0.0.1']
    
    def process_request(self,request):
        ip=request.META.get('REMOTE_ADDR')
        if ip in self.Blocked_IPs:
            return HttpResponse('Your IP has been blocked !')
            
   