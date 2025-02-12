from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from django_ratelimit.exceptions import Ratelimited

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_urls = [
            reverse('login'), 
        ]

        if not request.user.is_authenticated and request.path not in exempt_urls:
            return redirect('login') 

        response = self.get_response(request)
        return response

class RatelimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Ratelimited:
            return JsonResponse({"error": "Too many requests"}, status=429)
