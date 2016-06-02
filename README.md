# django-layered-cache

A coherent, layered cache solution for Django.

Provides a way to specify a single cache that is actually a hierarchy of underlying caches.  This can be useful for many situations:

- using an in-memory cache to support high throughput of cache operations within a request, while distributing the cached results for other works to take advantage of
- using a smaller distributed in-memory cache to support hot items, while more warm items fall back to be cached on local disk
