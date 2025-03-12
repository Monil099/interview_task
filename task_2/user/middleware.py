import time
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import status

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 10
        self.time = 60

    def get_client_ip(self, request):
        ip = request.META.get("REMOTE_ADDR")
        return ip

    def __call__(self, request, *args, **kwds):
        ip = self.get_client_ip(request)
        key = f"rate_limit:{ip}"
        data = cache.get(key)

        if data is None:
            cache.set(key=key, value={"count": 1, "start_time": time.time()}, timeout=self.time)
        else:
            if data["count"] > self.rate_limit:
                return JsonResponse({"error": "Too many requests. Try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            data["count"] += 1
            cache.set(key=key, value=data, timeout=self.time - (time.time() - data["start_time"]))

        return self.get_response(request)