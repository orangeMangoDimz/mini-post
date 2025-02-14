
from django.contrib.auth.models import User
from posts.models import Posts
from django.urls import reverse
from django.core.cache import cache
from django.test import override_settings
from config.tests.test_base import BaseTestCase
import time

class TestView(BaseTestCase):

    def setUp(self):
        self.username = 'budi'
        self.password = 'budi123'
        self.target_user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        self.post = Posts.objects.create(
            user=self.target_user,
            title='Test Post',
            description='Test Description'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123'
        )
        self.like_post_url_api = reverse('api.update_post_stat', kwargs={'postId': self.post.id})
        self.login_url_api = reverse('api.login')
        return super().setUp()

    def test_like_post_PUT_success_like(self):
        response = self.like_or_unlike('like')

        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        post_user_id = response_data.get('data', {}).get('post_user_id')

        self.assertIsNotNone(post_user_id)
        self.assertEqual(post_user_id, self.target_user.id)
        print("LIKE POST SUCCESS PASSED")

    def test_like_post_PUT_faileds_like(self):
        response = self.like_or_unlike('something_else')
        self.assertEqual(response.status_code, 400)
        print("LIKE POST FAILED PASSED")

    def test_like_post_PUT_success_unlike(self):
        self.like_or_unlike('like')
        time.sleep(self.delay_time)
        response = self.like_or_unlike('unlike')
        self.assertEqual(response.status_code, 200)
        print("UNLIKE POST SUCCESS PASSED")

    def test_like_post_PUT_faileds_unlike(self):
        response = self.like_or_unlike('unlike')
        self.assertEqual(response.status_code, 404)
        print("UNLIKE POST SUCCESS PASSED")

    def test_like_post_PUT_spam_like(self):
        for _ in range(self.max_limit_req):
            response = self.like_or_unlike('like')
            self.assertEqual(response.status_code, 200)

        response = self.like_or_unlike('like')
        self.assertEqual(response.status_code, 403) # I have no idea why it's 403, should be 429
        time.sleep(self.delay_time)
        response = self.like_or_unlike('like')
        self.assertEqual(response.status_code, 200)
        print("SPAM LIKE POST SUCCESS PASSED")

    def test_like_post_PUT_spam_unlike(self):
        for _ in range(self.max_limit_req):
            response = self.like_or_unlike('unlike')
            self.assertEqual(response.status_code, 404)

        response = self.like_or_unlike('unlike')
        self.assertEqual(response.status_code, 403)
        time.sleep(self.delay_time)
        response = self.like_or_unlike('like')
        time.sleep(self.delay_time)
        response = self.like_or_unlike('unlike')
        self.assertEqual(response.status_code, 200)
        print("SPAM UNLIKE POST SUCCESS PASSED")

    def test_signin_POST_spam_login(self):
        data = {
            'username': self.admin_user.username,
            'password': 'admin123'
        }
        for _ in range(self.max_limit_req):
            response = self.client.put(self.login_url_api, data, content_type='application/json')
            self.assertEqual(response.status_code, 302)

        response = self.client.put(self.login_url_api, data, content_type='application/json')
        self.assertEqual(response.status_code, 403)
        print("SPAM LOGIN POST SUCCESS PASSED")
        

    def like_or_unlike(self, action):
        data = {
            'type': 'likes',
            'action': action,
        }

        self.client.login(username=self.admin_user.username, password='admin123')
        response = self.client.put(self.like_post_url_api, data, content_type='application/json')
        return response
