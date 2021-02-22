from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tweet
from rest_framework.test import APIClient

User = get_user_model()

class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="khaled", password="ababababababa")
        Tweet.objects.create(content="my first test tweet", user=self.user)
        Tweet.objects.create(content="my second test tweet", user=self.user)
        Tweet.objects.create(content="my third test tweet", user=self.user)
        Tweet.objects.create(content="my fourth test tweet", user=self.user)
        Tweet.objects.create(content="my 5th test tweet", user=self.user)
        
    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content="my first test tweet", user=self.user)
        self.assertEqual(tweet_obj.id, 6)
        self.assertEqual(tweet_obj.user, self.user)
        
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='ababababababa')
        return client
    
    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("")
        self.assertEqual(response.status_code, 200)
      #  self.assertEqual(len(response.json()), 1)
        
    def tweet_action_like(self):
        client = self.get_client()
        response = client.post("/action/", {"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get('likes')
        self.assertEqual(like_count, 1)
      #  self.assertEqual(len(response.json()), 1)
      
    def tweet_action_unlike(self):
        client = self.get_client()
        response = client.post("/action/", {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/action/", {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get('likes')
        self.assertEqual(like_count, 1)
        