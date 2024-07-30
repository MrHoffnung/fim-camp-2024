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
    # post management
    path("post/new", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/update/", PostEditView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path('create_newsletter/', views.create_newsletter, name='create_newsletter'),
    path('newsletter_overview/', views.newsletter_overview, name='newsletter_overview'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
] 