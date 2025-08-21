import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('django.request')

class JWTAuthLoggingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path == '/api/token/':
            logger.info(f"POST /api/token/ {response.status_code} IP:{request.META.get('REMOTE_ADDR')}")
        return response

