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

from blog.forms import UserRegisterForm, NewsletterForm
from blog.models import Post, Profile, Newsletter, Follow
from django.contrib.auth.decorators import login_required
from .utils import has_user_followed, has_user_subscribed, has_user_liked_post

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

        # Liste der modifizierten Posts
        modified_posts = []
        for post in show_posts.object_list:
            creator_as_user = post.creator.user
            post.has_followed = has_user_followed(self.request.user, creator_as_user) if self.request.user.is_authenticated else False
            modified_posts.append(post)

        # Neue Paginierung mit den modifizierten Posts
        modified_paginator = Paginator(modified_posts, self.posts_per_page)
        try:
            modified_show_posts = modified_paginator.page(page)
        except PageNotAnInteger:
            modified_show_posts = modified_paginator.page(1)
        except EmptyPage:
            modified_show_posts = modified_paginator.page(modified_paginator.num_pages)

        context["posts"] = modified_show_posts
        context["only_followed"] = self.request.GET.get("only_followed", False)
        context["last_users"] = User.objects.order_by("-date_joined")[:10]

        # Debugging: Überprüfen Sie den finalen Kontext
        print(f"Context posts: {context['posts'].object_list}")
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
    fields = ["title", "content"]
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
        'is_following': has_user_followed(request.user, profile.user),
    })


@login_required
def create_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.user = request.user
            newsletter.save()
            return redirect('newsletter_overview')
    else:
        form = NewsletterForm()
    return render(request, 'blog/newsletter/create_newsletter.html', {'form': form})

@login_required
def newsletter_overview(request):
    newsletters = Newsletter.objects.filter(user=request.user)
    return render(request, 'blog/newsletter/newsletter_overview.html', {'newsletters': newsletters})

@login_required
def follow_user(request, user_id):
    followed_user = get_object_or_404(User, id=user_id)
    Follow.objects.create(user=request.user, followed_user=followed_user)
    username = followed_user.username

    referer = request.META.get('HTTP_REFERER')

    if referer.endswith('blog/'):
        return redirect('index')
    elif "profile" in referer:
        return redirect('profile_view', username=username)


@login_required
def unfollow_user(request, user_id):
    followed_user = get_object_or_404(User, id=user_id)
    Follow.objects.filter(user=request.user, followed_user=followed_user).delete()
    print(f"Unfollowed {followed_user.username}")
    username = followed_user.username

    referer = request.META.get('HTTP_REFERER')

    if referer.endswith('blog/'):
        return redirect('index')
    elif "profile" in referer:
        return redirect('profile_view', username=username)
