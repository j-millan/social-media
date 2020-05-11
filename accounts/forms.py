from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from social.models import Profile

class UserForm(UserCreationForm):
	email = forms.EmailField(
		max_length=130,
		required=True,
		widget=forms.EmailInput()
	)

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
	birth_date = forms.DateField(widget=forms.SelectDateWidget(
		empty_label=['Year', 'Month', 'Day'],
		years=range(1975, 2012)
	))

	class Meta:
		model = Profile
		fields = ['birth_date', 'country'] 