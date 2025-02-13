from django.test import TestCase, Client
from django.contrib.auth.models import User
from posts.models import Posts
from django.urls import reverse
from django.core.cache import cache
from django.test import override_settings
import time

@override_settings(CACHES={
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
})

class BaseTestCase(TestCase):

    def setUp(self):
        cache.clear()
        self.client = Client()
        self.max_limit_req = 5
        self.delay_time = 5.1
        time.sleep(self.delay_time) 
        return super().setUp()

    def tearDown(self):
        cache.clear()
        Posts.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()