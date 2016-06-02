DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = [
    'django_nose',
    'tests.testapp',
]

ROOT_URLCONF = 'tests.urls'

SECRET_KEY = "supersecret"

CACHES = {
    'default': {
      'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    },
    'simple_in_mem': {
      'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
      'LOCATION': 'simple_in_mem'
    },
    'simple_shared_mem': {
      'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
      'LOCATION': 'simple_shared_mem'
    },
    'simple_layered': {
        'BACKEND': 'layered_cache.LayeredCache',
        'LEVELS': ['simple_in_mem', 'simple_shared_mem']
    },
    'complex_dummy': {
      'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
      'LOCATION': 'complex_dummy'
    },
    'complex_shared_mem': {
      'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
      'LOCATION': 'complex_shared_mem'
    },
    'complex_layered': {
        'BACKEND': 'layered_cache.LayeredCache',
        'LEVELS': ['complex_dummy', 'complex_shared_mem']
    },

}
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
MIDDLEWARE_CLASSES = tuple()
