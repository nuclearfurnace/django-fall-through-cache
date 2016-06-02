from django.core.cache.backends.base import DEFAULT_TIMEOUT, BaseCache
from django.core.cache import caches
from django.core.exceptions import ImproperlyConfigured


class LayeredCache(BaseCache):
    def __init__(self, name, params):
        super(LayeredCache, self).__init__(params)
        self.levels = params.get('levels', params.get('LEVELS', []))
        if len(self.levels) == 0:
          raise ImproperlyConfigured("no levels configured for '{}'".format(name))

    def _get_underlying_cache(self, name):
        """
        Gets the cache object mapped to the given name from the configured
        Django caches. If the named cache does not exist,
        InvalidCacheBackendError will be raised.
        """
        return caches[name]

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        """
        Set a value in the cache if the key does not already exist. If
        timeout is given, that timeout will be used for the key; otherwise
        the default cache timeout will be used.

        This is applied to all configured cache levels.  Does not fail if
        intermediate error occurs during operation.

        Returns True if the value was stored, False otherwise.
        """
        succeeded = True
        for level in self.levels:
            underlying_cache = self._get_underlying_cache(level)
            if not underlying_cache.add(key, value, timeout=timeout, version=version):
                succeeded = False
        return succeeded

    def get(self, key, default=None, version=None):
        """
        Fetch a given key from the cache. If the key does not exist, return
        default, which itself defaults to None.

        All configured cache levels will be checked in order, first to last.
        """
        for level in self.levels:
            underlying_cache = self._get_underlying_cache(level)
            result = underlying_cache.get(key, version=version)
            if result is not None:
                return result

        return default

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        """
        Set a value in the cache. If timeout is given, that timeout will be
        used for the key; otherwise the default cache timeout will be used.

        This is applied to all configured ache levels.  Does not fail if
        intermediate error occurs during operation.
        """
        for level in self.levels:
            underlying_cache = self._get_underlying_cache(level)
            underlying_cache.set(key, value, timeout=timeout, version=version)

    def delete(self, key, version=None):
        """
        Delete a key from the cache, failing silently.

        This is applied to all configured cache levels.  Does not fail if
        intermediate error occurs during operation.
        """
        for level in self.levels:
            underlying_cache = self._get_underlying_cache(level)
            underlying_cache.delete(key, version=version)

    def has_key(self, key, version=None):
        """
        Returns True if the key is in the cache and has not expired.
        """
        for level in self.levels:
            underlying_cache = self._get_underlying_cache(level)
            if underlying_cache.has_key(key, version=version):
              return True

        return False

    def get_many(self, keys, version=None):
        """
        Fetch a bunch of keys from the cache. For certain backends (memcached,
        pgsql) this can be *much* faster when fetching multiple values.

        The results are the sum of the unique keys returned by all cache
        levels.  Any key that is already present in the results will have
        the value from the deepest cache i.e. if cache #1 and cache #2  --
        which are checked in that order -- both have the same key, cache #2
        will be the cache that "wins" for the given key.

        Returns a dict mapping each key in keys to its value. If the given
        key is missing, it will be missing from the response dict.
        """
        results = {}
        for level in self.levels:
            underlying_cache = self._get_underlying_cache(level)
            result = underlying_cache.get_many(keys, version=version)
            results.update(result)

        return results

    def set_many(self, data, timeout=DEFAULT_TIMEOUT, version=None):
        """
        Set a bunch of values in the cache at once from a dict of key/value
        pairs.  For certain backends (memcached), this is much more efficient
        than calling set() multiple times.

        If timeout is given, that timeout will be used for the key; otherwise
        the default cache timeout will be used.
        """
        for level in self.levels:
            underlying_cache = self._get_underlying_cache(level)
            underlying_cache.set_many(data, timeout=timeout, version=version)

    def delete_many(self, keys, version=None):
        """
        Delete a bunch of values in the cache at once. For certain backends
        (memcached), this is much more efficient than calling delete() multiple
        times.

        This is applied to all configured cache levels.  Does not fail if
        intermediate error occurs during operation.
        """
        for level in self.levels:
            underlying_cache = self._get_underlying_cache(level)
            underlying_cache.delete_many(keys, version=version)

    def clear(self):
        """
        Remove *all* values from the cache at once.

        This is applied to all configured cache levels.  Does not fail if
        intermediate error occurs during operation.
        """
        for level in self.levels:
            underlying_cache = self._get_underlying_cache(level)
            underlying_cache.clear()

