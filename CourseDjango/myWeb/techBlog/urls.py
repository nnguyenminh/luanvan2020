from django.urls import path

from . import views

urlpatterns = [
	path('', views.homeView, name="home"),
	path('article/', views.articleView, name="article"),
	path('about/', views.aboutView, name="about"),
	path('blog/', views.blogView, name="blog"),
	path('contact/', views.contactView, name="contact"),
]