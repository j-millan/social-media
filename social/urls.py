from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
	path('', views.HomeView.as_view(), name='home'),
	path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_details'),
	path('user-profile/<int:pk>', views.ProfileDetailView.as_view(), name='user_profile')
]