from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Profile, Post, Comment
from .forms import PostForm, CommentForm


@method_decorator(login_required, name='dispatch')
class HomeView(CreateView):
	model = Post
	form_class = PostForm
	template_name = 'social/home.html'

	def form_valid(self, form):
		post = form.save(commit=False)
		post.created_by = self.request.user.profile
		post.save()
		return redirect('social:home')

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data()
		queryset = []

		for post in Post.objects.order_by('-created_at'):
			if post.created_by.is_friends_with(self.request.user.profile):
				queryset.append(post)

		context['posts'] = queryset
		return context

@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView):
    model = Profile
    template_name = "social/user_profile.html"

@method_decorator(login_required, name='dispatch')
class PostDetailView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'social/post_details.html'

    def form_valid(self, form):
    	comment = form.save(commit=False)
    	comment.created_by = self.request.user.profile
    	comment.post = get_object_or_404(Post, pk=self.kwargs['pk'])
    	comment.save()
    	return redirect('social:post_details', pk=comment.post.pk)

    def get_context_data(self, **kwargs):
    	context = super(PostDetailView, self).get_context_data()
    	context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
    	return context





































