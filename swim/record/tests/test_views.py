from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from record import views, models


class TestIndex(TestCase):
    def setUp(self):
        username='testuser'
        password='test1234test'
        self.user = User.objects.create(username=username, password=password)
        models.User_Info.objects.create(user=self.user, cource=4)

    def test_authenticated(self):
        client = Client()
        client.force_login(self.user)
        res = client.get(reverse('index'))
        self.assertTemplateUsed(res, 'record/index.html')
        self.assertContains(res, self.user.username)
        self.assertEqual(res.context['username'], self.user.username)

    def test_not_authenticated(self):
        client = Client()
        res = client.get(reverse('index'))
        self.assertFalse(self.user.username in res)
        self.assertRedirects(res, '/record/login/?next=/record/')
        
    def tearDown(self):
        pass
