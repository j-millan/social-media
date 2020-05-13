from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from social.models import Profile, Post, Comment
from social.views import PostDetailView 
from social.forms import CommentForm

class PostDetailsViewTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='user1', first_name='Jhonattan', last_name='Millán', email='email@email.com', password='123password123')
		self.client.login(username='user1', password='123password123')
		Profile.objects.create(user=self.user)
		
		self.post = Post.objects.create(message="Lorem ipsum dolor sit amet.", created_by=self.user.profile)
		self.url = reverse('social:post_details', kwargs={'pk': 1})
		self.response = self.client.get(self.url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_not_found(self):
		url = reverse('social:post_details', kwargs={'pk': 99})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 404)

	def test_view_function(self):
		view = resolve('/post/1/')
		self.assertEquals(view.func.view_class, PostDetailView)

	def test_contains_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_contains_comment_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, CommentForm)

	def test_form_inputs(self):
		self.assertContains(self.response, "<textarea")

class SuccessfulCommentTets(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='user1', first_name='Jhonattan', last_name='Millán', email='email@email.com', password='123password123')
		self.client.login(username='user1', password='123password123')
		Profile.objects.create(user=self.user)
		
		data = {
			'message': 'This is a comment.'
		}

		self.post = Post.objects.create(message="Lorem ipsum dolor sit amet.", created_by=self.user.profile)
		self.url = reverse('social:post_details', kwargs={'pk': 1})
		self.response = self.client.post(self.url, data)
		
	def test_redirection(self):
		self.assertRedirects(self.response, self.url)

	def test_comment_creation(self):
		self.assertTrue(Comment.objects.exists())

class InvalidCommentTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='user1', first_name='Jhonattan', last_name='Millán', email='email@email.com', password='123password123')
		self.client.login(username='user1', password='123password123')
		Profile.objects.create(user=self.user)
		
		data = {'message': ''}

		self.post = Post.objects.create(message="Lorem ipsum dolor sit amet.", created_by=self.user.profile)
		self.url = reverse('social:post_details', kwargs={'pk': 1})
		self.response = self.client.post(self.url, data)

	def test_redirection(self):
		self.assertEquals(self.response.status_code, 200)

	def test_form_errors(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)