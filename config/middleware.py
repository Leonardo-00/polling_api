import re
from django.core.exceptions import DisallowedHost

class RegexHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_domain_re = re.compile(r'^.+\.vercel\.app$')

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        if self.allowed_domain_re.match(host) or host in ['127.0.0.1', 'localhost']:
            return self.get_response(request)
        raise DisallowedHost(f"Invalid host: {host}")
    

class AllowVercelSubdomains:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_domain_re = re.compile(r'^.+\.vercel\.app$')

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        if self.allowed_domain_re.match(host) or host in ['127.0.0.1', 'localhost']:
            return self.get_response(request)
        raise DisallowedHost(f"Invalid host: {host}")