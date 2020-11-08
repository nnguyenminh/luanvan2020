from django.urls import path
from blog import views

urlpatterns = [
    path('api/post/', views.add_post),
    path('api/update_post/<int:id>', views.update_post),
    path('api/delete_post/<int:id>', views.delete_post),
    path('api/post/search/<str:id>', views.read_post),
    path('api/post/all', views.read_post_all),
    path('home/', views.home, name="home"),
    path('home/page=<int:page>', views.home),
    path('article/', views.article, name="article"),
    path('about/', views.about, name="about"),
    path('blog/', views.blog, name="blog"),
    path('contact/', views.contact, name="contact"),
    path('post/<str:id>', views.post, name="post"),
]
