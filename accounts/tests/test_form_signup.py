from django.test import TestCase
from ..forms import UserForm

class SignUpFormTests(TestCase):
	def test_form_fields(self):
		form = UserForm()
		efields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
		afields = list(form.fields)
		self.assertSequenceEqual(efields, afields) 