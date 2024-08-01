from django.urls import include, path

from . import views
from .views import PostCreateView, PostDeleteView, PostEditView, UserUpdateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.PostListView.as_view(), name="index"),
    # user management
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="blog_logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("user/<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
    path("profile/<str:username>", views.profile_view, name="profile_view"),
    path("profile/<int:pk>/update", views.ProfileUpdateView.as_view(), name="profile_update"),
    # post management
    path("post/new", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/update/", PostEditView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path('follow/<int:user_id>/', views.follow_view, name='follow_view'),
    path('upvote/<int:post_id>/', views.upvote_view, name='upvote_view'),
    path('downvote/<int:post_id>/', views.downvote_view, name='downvote_view'),
    path('comment/<int:post_id>/', views.add_comment_view, name='add_comment_view'),
    path('chat', views.chat_view, name='chat_view'),
] 