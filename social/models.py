from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django_countries import fields as country_fields
from django.core.cache import cache
from Project import settings
from django.db.models import Q
import datetime

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_picture = models.ImageField(upload_to='img/profilepictures/', default='img/profilepictures/default-profile-picture.png')
	header_picture = models.ImageField(upload_to='img/headerpictures/', default='img/headerpictures/default-header-picture.png')
	country = country_fields.CountryField()
	birth_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
	gender_list = (('M', 'Male'), ('F', 'Female'))
	gender = models.CharField(max_length=1, choices=gender_list, null=True)
	follows = models.ManyToManyField('Profile', related_name='followed_by')

	def get_full_name(self):
		return f'{self.user.first_name} {self.user.last_name}'

	def get_short_name(self):
		last_name = self.user.last_name[0]
		return f'{self.user.first_name} {last_name}.'

	def get_friend_requests(self):
		query = self.friend_requests.order_by('-pk')
		return query

	def has_friend_requests(self):
		return True if len(self.friend_requests.all()) > 0 else False

	def has_friends(self):
		return True if len(Friendship.objects.filter(Q(creator=self) | Q(friend=self))) > 0 else False

	def is_friends_with(self, friend_profile):
		profiles = [self, friend_profile]
		friend = Friendship.objects.filter(creator__in=profiles, friend__in=profiles)
		return True if friend.exists() else False
	
	def get_friends(self):
		friends = []
		for f in list(Friendship.objects.filter(Q(creator=self) | Q(friend=self))):
			friends.append(f.creator if f.creator != self else f.friend)

		return friends

	def get_online_friends(self):
		friends = []
		for f in self.get_friends():
			if f.online:
				friends.append(f)

		return friends

	def get_offline_friends(self):
		friends = []
		for f in self.get_friends():
			if not f.online:
				friends.append(f)

		return friends

	def last_seen(self):
		return cache.get('seen_%s' % self.user.username)

	def online(self):
		if self.last_seen():
			now = datetime.datetime.now()
			if now > self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
				return False
			else:
				return True
		else:
			return False

	def __str__(self):
		return self.get_short_name()

class Post(models.Model):
	message = models.TextField(blank=True)
	cover = models.ImageField(upload_to='img/postcovers/', blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)

	def has_comments(self):
		return True if len(self.comments.all()) > 0 else False

	def __str__(self):
		return f'By {self.created_by.get_full_name()}: {self.message}'

class Comment(models.Model):
	message = models.TextField()
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Profile, related_name='+', on_delete=models.CASCADE)

	def __str__(self):
		return self.message
		
class FriendRequest(models.Model):
	sender = models.ForeignKey(Profile, related_name='request_senders', on_delete=models.CASCADE)
	friend = models.ForeignKey(Profile, related_name='friend_requests', on_delete=models.CASCADE)

	def __str__(self):
		return 'From {0} to {1}.'.format(self.sender.get_short_name(), self.friend.get_short_name())

class Friendship(models.Model):
	friends_since = models.DateTimeField(auto_now_add=True)
	creator = models.ForeignKey(Profile, related_name='+', on_delete=models.CASCADE)
	friend = models.ForeignKey(Profile, related_name='friendships', on_delete=models.CASCADE)

	def __str__(self):
		return '{0}  and {1}, since {2}.'.format(self.creator.get_short_name(), self.friend.get_short_name(), self.friends_since)