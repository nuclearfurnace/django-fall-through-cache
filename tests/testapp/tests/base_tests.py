# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import wraps
import time
import sys

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


from django.core.cache import caches, get_cache
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
try:
    from django.test import override_settings
except ImportError:
    from django.test.utils import override_settings


SIMPLE_CACHES = ['simple_in_mem', 'simple_shared_mem']


def clear_caches(cache_names):
    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            # Clear all configured caches.
            for cache_name in cache_names:
                cache = get_cache(cache_name)
                cache.clear()

            return method(self, *args, **kwargs)
        return wrapper
    return decorator


class BaseLayeredCacheTestCase(TestCase):
    @clear_caches(SIMPLE_CACHES)
    def test_simple_set(self):
        """
        Simple test to make sure we can set/get.

        Assert the value is present in both underlying caches.
        """
        coherent_cache = get_cache('simple_layered')
        self.assertEqual(coherent_cache.get("key"), None)
        coherent_cache.set("key", "value")
        self.assertEqual(coherent_cache.get("key"), "value")

        first_level = get_cache('simple_in_mem')
        second_level = get_cache('simple_shared_mem')
        self.assertEqual(first_level.get("key"), "value")
        self.assertEqual(second_level.get("key"), "value")

        coherent_cache.set("key", "new_value")
        self.assertEqual(coherent_cache.get("key"), "new_value")

        first_level = get_cache('simple_in_mem')
        second_level = get_cache('simple_shared_mem')
        self.assertEqual(first_level.get("key"), "new_value")
        self.assertEqual(second_level.get("key"), "new_value")

    @clear_caches(SIMPLE_CACHES)
    def test_simple_add(self):
        """
        Simple test to make sure we can add/get.

        Assert the value is present in both underlying caches.
        """
        coherent_cache = get_cache('simple_layered')
        self.assertEqual(coherent_cache.get("key"), None)
        coherent_cache.add("key", "value")
        self.assertEqual(coherent_cache.get("key"), "value")

        first_level = get_cache('simple_in_mem')
        second_level = get_cache('simple_shared_mem')
        self.assertEqual(first_level.get("key"), "value")
        self.assertEqual(second_level.get("key"), "value")

    @clear_caches(SIMPLE_CACHES)
    def test_simple_double_add(self):
        """
        Simple test to make sure we can add/get and then add/get again without error.

        Assert the value is present in both underlying caches.
        """
        coherent_cache = get_cache('simple_layered')
        self.assertEqual(coherent_cache.get("key"),  None)
        coherent_cache.add("key", "value")
        self.assertEqual(coherent_cache.get("key"), "value")

        first_level = get_cache('simple_in_mem')
        second_level = get_cache('simple_shared_mem')
        self.assertEqual(first_level.get("key"), "value")
        self.assertEqual(second_level.get("key"), "value")

        # Since it already exists, we expect to get 'value' back.
        coherent_cache.add("key", "new_value")
        self.assertEqual(coherent_cache.get("key"), "value")

        first_level = get_cache('simple_in_mem')
        second_level = get_cache('simple_shared_mem')
        self.assertEqual(first_level.get("key"), "value")
        self.assertEqual(second_level.get("key"), "value")

    @clear_caches(SIMPLE_CACHES)
    def test_simple_delete(self):
        """
        Simple test to make sure we can set/get/delete without error.

        Assert the value is present in both underlying caches in between
        and that the caches are clear after the delete.
        """
        coherent_cache = get_cache('simple_layered')
        self.assertEqual(coherent_cache.get("key"),  None)
        coherent_cache.set("key", "kablam")
        self.assertEqual(coherent_cache.get("key"), "kablam")

        first_level = get_cache('simple_in_mem')
        second_level = get_cache('simple_shared_mem')
        self.assertEqual(first_level.get("key"), "kablam")
        self.assertEqual(second_level.get("key"), "kablam")

        coherent_cache.delete("key")
        self.assertEqual(coherent_cache.get("key"), None)

        first_level = get_cache('simple_in_mem')
        second_level = get_cache('simple_shared_mem')
        self.assertEqual(first_level.get("key"), None)
        self.assertEqual(second_level.get("key"), None)



class ConfigurationTestCase(TestCase):
    @override_settings(
        CACHES={
            'default': {
                'BACKEND': 'layered_cache.LayeredCache'
            },
        }
    )
    def test_missing_configured_levels(self):
        with self.assertRaises(ImproperlyConfigured):
            get_cache('default')

