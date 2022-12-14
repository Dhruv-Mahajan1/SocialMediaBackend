import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


from .models import User
from .models import Post, Like, Comment,Following


class UserProfileAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.user3= User.objects.create_user(username='user3', password='password3')

    def test_get_user_profile(self):
        self.client.login(username='user1', password='password1')
        response= self.client.get('/api/userprofile')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['User Name'], 'user1')

    def test_follow_user(self):
        self.client.login(username='user1', password='password1')
        # User1 follows User2
        response = self.client.post('/api/follow/user2')
        self.assertEqual(response.status_code, 200)

        # Check that user1 appears in user2's followers
        user2 = User.objects.get(username='user2')
        followers_id_list = Following.objects.filter(userfollowed=user2).values_list('user', flat=True)
        followers_user_list = User.objects.filter(id__in=followers_id_list).values('username')
        self.assertIn({'username':self.user1.username}, followers_user_list)

    def test_unfollow_user(self):
        self.client.login(username='user1', password='password1')
        self.client.post('/api/follow/user2')
        response = self.client.post('/api/unfollow/user2')
        self.assertEqual(response.status_code, 200)

        user2 = User.objects.get(username='user2')
        followers_id_list = Following.objects.filter(userfollowed=user2).values_list('user', flat=True)
        followers_user_list = User.objects.filter(id__in=followers_id_list).values('username')
        self.assertNotIn({'username':self.user1.username}, followers_user_list)

class TestPostAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.user3= User.objects.create_user(username='user3', password='password3')

    def test_add_post(self):
        # Test uploading a new post
        self.client.login(username='user1', password='password1')
        response = self.client.post('/api/addpost', {"title":"test","content":"this is the contetn"},format='json')
        self.assertEqual(response.status_code, 201)

    def test_delete_post(self):
        # First, upload a new post to delete
        self.client.login(username='user1', password='password1')
        response = self.client.post('/api/addpost', {"title":"test","content":"this is the contetn"},format='json')
        self.assertEqual(response.status_code, 201)
        post_id = response.data['Post_id']

        # Test deleting the post
        response = self.client.post(f'/api/deletepost/{post_id}')
        self.assertEqual(response.status_code, 204)

    def test_like_post(self):
        # First, upload a new post to like
        self.client.login(username='user1', password='password1')
        response = self.client.post('/api/addpost', {"title":"test","content":"this is the contetn"},format='json')
        self.assertEqual(response.status_code, 201)
        post_id = response.data['Post_id']

        # Test liking the post
        response = self.client.post(f'/api/likepost/{post_id}')
        self.assertEqual(response.status_code, 201)

    def test_unlike_post_and_comment(self):
        # Create a user to test the API with
        self.client.login(username='user1', password='password1')
        response = self.client.post('/api/addpost', {"title":"test","content":"this is the contetn"},format='json')
        self.assertEqual(response.status_code, 201)
        post_id = response.data['Post_id']
        
        # Like the post
        post=Post.objects.get(id=post_id)
        
        response = self.client.post(f'/api/likepost/{post_id}')
        like=Like.objects.get(post=post_id)
        self.assertEqual(like.likes, 1)

        # Test the unlike feature
        response = self.client.post('/api/dislikepost/{}'.format(post.id))
        self.assertEqual(response.status_code, 201)
        like=Like.objects.get(post=post_id)
        self.assertEqual(like.likes, 0)
        self.assertEqual(like.dislikes, 1)

        # Test the comment feature
        response = self.client.post('/api/addcomment/{}'.format(post.id), {'content': 'Test comment'},format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(post.comments.count(), 1)
        self.assertEqual(post.comments.first().content, 'Test comment')


