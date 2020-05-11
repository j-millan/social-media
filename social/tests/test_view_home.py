from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from ..models import Profile, Post, Friendship
from ..views import HomeView

class HomeViewTests(TestCase):
	def setUp(self):
		User.objects.create_user(username='jmillan0', first_name='Jhonattan', last_name='Millán' , email='mail@google.com', password='mypassword21')
		self.client.login(username='jmillan0', password='mypassword21')
		url = reverse('social:home')
		self.response = self.client.get(url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve('/')
		self.assertEquals(view.func.view_class, HomeView)

	def test_contains_search_bar(self):
		self.assertContains(self.response, '<input class="form-control" type="text" id="namefield" placeholder="Search people">')

class FeedPostsTests(TestCase):
	def setUp(self):
		user = User.objects.create_user(username='jmillan0', first_name='Jhonattan', last_name='Millán' , email='mail@google.com', password='mypassword21')
		self.friend = User.objects.create_user(username='badcc', first_name='Bad', last_name='Badimo',email='rblx@outlook.com', password='contraseña98989')
		random = User.objects.create_user(username='brandon_b', first_name='Obscured', last_name='Entity', email='booga@booga.com', password='thefireisland')
		
		self.friend_post = Post.objects.create(message='Lorem ipsum dolor sit amet.', created_by=self.friend.profile)
		Post.objects.create(message='Optio totam animi numquam facere ratione iure.', created_by=random.profile)
		Friendship.objects.create(creator=self.friend.profile, friend=user.profile)

		self.client.login(username='jmillan0', password='mypassword21')

		url = reverse('social:home')
		self.response = self.client.get(url)

	def test_friend_post(self):
		pks = [post.pk for post in self.response.context.get('posts')]
		posts = Post.objects.filter(pk__in=pks).filter(created_by=self.friend.profile)
		self.assertTrue(posts.exists())
		self.assertContains(self.response, self.friend_post.message)