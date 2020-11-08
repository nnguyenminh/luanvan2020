from django.urls import path

from . import views

urlpatterns = [
	path('article/', views.articleView, name="article"),
]