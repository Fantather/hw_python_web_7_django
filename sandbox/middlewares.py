from django.http import HttpResponseForbidden
from django.core.cache import cache

# Ограничение применяется только для пути /sandbox/restricted-area
class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.path.startswith('/sandbox/restricted-area/'):
            ip_address = request.META.get('REMOTE_ADDR')
            cache_key = f'rate_limit_{ip_address}'
            
            request_count = cache.get(cache_key, 0)
            
            if request_count >= 5:
                return HttpResponseForbidden("Превышен лимит запросов: максимум 5 в минуту.")
            
            # Увеличиваем счетчик и обновляем/устанавливаем таймер на 60 секунд
            cache.set(cache_key, request_count + 1, timeout=60)

        response = self.get_response(request)
        return response