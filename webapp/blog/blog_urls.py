from django.urls import path
from blog import views

urlpatterns = [
    path('post/', views.add_post),
    path('update_post/<int:id>', views.update_post),
    path('delete_post/<int:id>', views.delete_post),
    path('post/search/<str:id>', views.read_post),
    path('read_post_all', views.read_post_all),
]

