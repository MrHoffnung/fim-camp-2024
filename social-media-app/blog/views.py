from typing import Any, Dict

import django.http
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q, QuerySet
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, TemplateView, UpdateView
from django.shortcuts import get_object_or_404

from blog.forms import UserRegisterForm
from blog.models import Post, Profile
from django.contrib.auth.decorators import login_required
from .utils import create_notification

################################################################################
# user management


def register(request: django.http.HttpRequest) -> django.http.HttpResponse:
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            messages.success(
                request, "Dein Account wurde erstellt! Du kannst dich jetzt anmelden."
            )
            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "registration/register.html", {"form": form})


def logout_view(request: django.http.HttpRequest) -> django.http.HttpResponse:
    logout(request)
    messages.info(request, "Abgemeldet!")
    return redirect("index")


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ["username", "email"]
    template_name = "blog/user/user_edit.html"

    def test_func(self) -> bool:
        user = self.get_object()
        return self.request.user == user

    def get_success_url(self) -> str:
        user: User = self.get_object()
        return reverse("profile", kwargs={"username": user.username})


################################################################################
# post management


class PostListView(TemplateView):
    template_name = "blog/index.html"
    posts_per_page = 5

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        posts = self._posts()
        paginator = Paginator(posts, self.posts_per_page)
        page = self.request.GET.get("page", 1)

        try:
            page = int(page)
        except ValueError:
            page = 1

        try:
            show_posts = paginator.page(page)
        except PageNotAnInteger:
            show_posts = paginator.page(1)
        except EmptyPage:
            show_posts = paginator.page(paginator.num_pages)


        context["posts"] = show_posts
        context["only_followed"] = self.request.GET.get("only_followed", False)
        context["latest_users"] = User.objects.order_by("-date_joined")[:10]
        context["latest_posts"] = Post.objects.order_by("-publication_date")[:10]

        return context
          

    def _posts(self) -> QuerySet[Post]:
        search_query = self.request.GET.get("search_query")

        if not search_query:
            posts = Post.objects.all()
        else:
            posts = Post.objects.filter(
                Q(title__icontains=search_query)
                | Q(content__icontains=search_query)
                | Q(creator__username__icontains=search_query)  # Korrigierte Zeile
            )

        return posts.order_by("-publication_date")

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ["bio", "birth_date", "profile_image"]
    template_name = "blog/user/profile_edit.html"

    def get_success_url(self) -> str:
        profile: Profile = self.get_object()
        return reverse("profile_view", kwargs={"username": profile.user.username})

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]
    success_url = reverse_lazy("index")
    template_name = "blog/post/create_post.html"

    def form_valid(self, form) -> HttpResponse:
        profile = Profile.objects.get(user=self.request.user)
        form.instance.creator = profile
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("index")
    template_name = "blog/post/confirm_delete.html"

    def test_func(self) -> bool:
        post: Post = self.get_object()
        return self.request.user == post.creator.user


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content", "image"]
    success_url = reverse_lazy("index")
    template_name = "blog/post/edit_post.html"

    def test_func(self) -> bool:
        post: Post = self.get_object()
        return self.request.user == post.creator.user


@login_required
def profile_view(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    return render(request, 'blog/user/profile.html', {
        'profile': profile,
    })




@login_required
def like_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    likes = post.likes.all()
    user = request.user
    if user in likes:
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    post.save()
    return redirect('index')

@login_required
def follow_view(request, user_id):
    profile = get_object_or_404(Profile, id=user_id)
    followers = profile.followers.all()
    user = request.user

    if user in followers:
        profile.followers.remove(user)
    else:
        profile.followers.add(user)
    profile.save()

    referer = request.META.get('HTTP_REFERER')

    if referer.endswith('blog/'):
        return redirect('index')
    elif "profile" in referer:
        return redirect('profile_view', username=user.username)

    