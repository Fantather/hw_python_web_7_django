import json

from django.core.cache import cache
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect
from django.views import View

# Create your views here.
class CacheItemDataView(View):
    def get(self, request:HttpRequest, item_id:int):
        cache_key = f'item_data{item_id}'

        data = cache.get(cache_key)

        if data is None:
            cache.set(cache_key, "Data", timeout=300)
            return HttpResponse(f"Значение по ID {item_id} было кешировано")
        
        return HttpResponse(f"Значение по ID {item_id} было получено из кеша")
    
class RestrictedPathView(View):
    def get(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        cache_key = f'rate_limit_{ip_address}'
        request_count = cache.get(cache_key, 1)

        return HttpResponse(f"Вы сделали {request_count} запросов из 5")

# 3. Нормализуем данные
class JsonNormalizeView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            raw_name = data.get('name', '')
            raw_age = data.get('age', 0)
            
            normalized_data = {
                "name": str(raw_name).capitalize(),
                "age": int(raw_age)
            }
            
            return JsonResponse(normalized_data)
            
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Некорректный формат JSON.")
        except ValueError:
            return HttpResponseBadRequest("Поле age должно быть числом.")
        
# 4 Проверяю с чего зашёл пользователь
class DeviceRoutingView(View):
    def get(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        if 'mobi' in user_agent:
            return redirect('/mobile-page/')
            
        return HttpResponse("Добро пожаловать на ПК версию")
    

# === 5 ===
data_dict = {
    "1": "Yes",
    "3": "No"
}

class DataGetView(View):
    def get(self, request, key):
        if key in data_dict:
            return JsonResponse({key: data_dict[key]})
        
        raise Http404("Ключ не найден")

class DataUpdateView(View):
    def post(self, request):
        try:
            new_data = json.loads(request.body)
            data_dict.update(new_data)

            return JsonResponse({
                "message": "Словарь успешно обновлён", 
                "current_state": data_dict
            })
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Ожидается валидный JSON"}, status=400)