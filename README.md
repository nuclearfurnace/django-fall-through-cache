# django-layered-cache

A coherent, layered cache solution for Django.

Provides a way to specify a single cache that is actually a hierarchy of underlying caches.  This can be useful for many situations:

- using an in-memory cache to support high throughput of cache operations within a request, while distributing the cached results for other workers to take advantage of
- having a small, distributed, in-memory cache that holds the hottest items, while warmer items can be served out of a larger, local disk-based cache
