from django.urls import path

from . import views

urlpatterns = [
	path('', views.homeView, name="home"),
	path('article/', views.homeView, name="article"),
	path('about/', views.homeView, name="about"),
	path('blog/', views.homeView, name="blog"),
	path('contact/', views.homeView, name="contact"),
]