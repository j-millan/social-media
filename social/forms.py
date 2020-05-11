from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Comment

class PostForm(forms.ModelForm):
	def clean(self):
		cleaned_data = super().clean()
		message = cleaned_data.get('message')
		cover = cleaned_data.get('cover')

		if not cover and not message:
			raise ValidationError('You must either add a message or choose an image to upload.')

	class Meta:
		model = Post
		fields = ['message', 'cover']
		widgets = {
			'message': forms.Textarea(attrs={'rows': 3, 'placeholder': "What's in your head?"}),
		}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ["message"]
		widgets = {
			'message': forms.Textarea(attrs={'rows': 2, 'placeholder': 'I like your post...'}),
		}