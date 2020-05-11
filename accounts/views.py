from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from social.models import Profile
from .forms import UserForm, ProfileForm

def sign_up(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			user = form.save()
			auth_login(request, user)
			return redirect('social:home')
	else:
		form = UserForm()
	return render(request, 'accounts/sign_up.html', {'form': form})



'''@method_decorator(login_required, name='dispatch')
def update_account(self, request):
	if request.method == 'POST':
		user_form = UserForm(request.post, instance=request.user)
		profile_form = UserForm(request.post, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()'''