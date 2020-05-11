from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from social.models import Profile
from ..views import sign_up
from ..forms import UserForm

class SignUpViewTests(TestCase):
	def setUp(self):
		url = reverse('accs:sign_up')
		self.response = self.client.get(url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve('/auth/signup/')
		self.assertEquals(view.func, sign_up)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, UserForm)

	def test_form_inputs(self):
		self.assertContains(self.response, '<input', 7)
		self.assertContains(self.response, 'type="text"', 3)
		self.assertContains(self.response, 'type="password"', 2)
		self.assertContains(self.response, 'type="email"', 	1)

class SuccessfulSignUpTests(TestCase):
	def setUp(self):
		data = {
			'first_name': 'Jhonattan',
			'last_name': 'Millán',
			'username': 'hellow21',
			'email': 'myemail@mail.com',
			'password1': 'holachaoadios',
			'password2': 'holachaoadios'
		}

		url = reverse('accs:sign_up')
		self.home_url = reverse('social:home')
		self.response = self.client.post(url, data)

	def test_redirection(self):
		self.assertRedirects(self.response, self.home_url)

	def test_user_creation(self):
		self.assertTrue(User.objects.exists())

	def test_profile_creation(self):
		self.assertTrue(Profile.objects.exists())

	def test_authentication(self):
		response = self.client.get(self.home_url)
		user = response.context.get('user')
		self.assertTrue(user.is_authenticated)

class InvalidSignUpTests(TestCase):
	def setUp(self):
		url = reverse('accs:sign_up')
		self.response = self.client.post(url, {})

	def test_sttus_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_form_errors(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)

	def test_dont_create_user(self):
		self.assertFalse(User.objects.exists())