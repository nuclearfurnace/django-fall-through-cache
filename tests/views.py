from django.core.cache import get_cache
from django.http import HttpResponse


def someview(request):
    cache = get_cache('layered')
    cache.set("foo", "bar")
    return HttpResponse("Pants")
