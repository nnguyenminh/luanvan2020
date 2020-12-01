from django.urls import path
from blog import views

urlpatterns = [
    path('api/post/', views.add_post),
    path('api/update_post/<int:id>', views.update_post),
    path('api/delete_post/<int:id>', views.delete_post),
    path('api/post/search/<str:id>', views.read_post),
    path('api/post/all', views.read_post_all),

    path('home/', views.home, name="home"),
    path('home/page=<int:page>', views.home, name="home"),
    path('category/<str:cat>', views.category, name="category"),
    path('contact/', views.contact, name="contact"),
    path('post/<str:id>', views.post, name="post"),
    path('search', views.search, name="search"),
    path('search/page=<int:page>', views.search, name="search"),
    path('post_comment', views.post_comment, name="post_comment"),
    path('load_comments/post=<int:id>', views.load_comments, name="load_comments"),
    path('get_recent_posts', views.get_recent_posts, name="get_recent_posts")
]
