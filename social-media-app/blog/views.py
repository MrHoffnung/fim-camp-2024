from typing import Any, Dict
from django.forms import BaseModelForm

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
from urllib.parse import urlencode

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
        return reverse("profile_view", kwargs={"username": user.username})


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
                | Q(creator__user__username__icontains=search_query)
            )

        return posts.order_by("-publication_date")

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ["bio", "birth_date", "profile_image"]
    template_name = "blog/user/profile_edit.html"

    def get_success_url(self) -> str:
        profile: Profile = self.get_object()
        return reverse("profile_view", kwargs={"username": profile.user.username})
    
    def get_form(self, form_class=None) -> BaseModelForm:
        form = super().get_form(form_class)
        form.fields["bio"].label = "Biographie"
        form.fields["birth_date"].label = "Geburtstag"
        form.fields["profile_image"].label = "Profilbild (quadratisch)"
        return form

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "image"]
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


def profile_view(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    tab = request.GET.get("tab")
    profile_posts = Post.objects.filter(creator=profile)
    upvoted_posts = Post.objects.filter(upvotes__in=[profile.user])
    downvoted_posts = Post.objects.filter(downvotes__in=[profile.user])


    if tab == None: tab = 'bio'

    return render(request, 'blog/user/profile.html', {
        'profile': profile,
        'tab': tab,
        'profile_posts': profile_posts,
        'upvoted_posts': upvoted_posts,
        'downvoted_posts': downvoted_posts
    })




@login_required
def upvote_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    upvotes = post.upvotes.all()
    user = request.user
    if user in upvotes:
        post.upvotes.remove(request.user)
    else:
        post.upvotes.add(request.user)

        if user in post.downvotes.all(): post.downvotes.remove(user)

    post.save()
    
    referer = request.META.get('HTTP_REFERER')

    if referer.endswith('blog/'):
        return redirect('index')
    elif "profile" in referer:
        return redirect(referer)
    
@login_required
def downvote_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    downvotes = post.downvotes.all()
    user = request.user
    if user in downvotes:
        post.downvotes.remove(request.user)
    else:
        post.downvotes.add(request.user)

        if user in post.upvotes.all(): post.upvotes.remove(user)
    post.save()
    
    referer = request.META.get('HTTP_REFERER')

    if referer.endswith('blog/'):
        return redirect('index')
    elif "profile" in referer:
        return redirect(referer)

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
        return redirect(referer)
    
def profile_view(request):
    profiles = Profile.objects.all()
    return render(request, 'blog/user/profile_list.html', {
        'profiles': profiles,
    })

@login_required
def add_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            profile = Profile.objects.get(user=request.user)
            post.comments.create(author=profile, content=content, post=post)
            post.save()
            
            create_notification(post.creator.user.id, 'System', f"{request.user.username} hat dir einen Kommentar hinterlassen", post.id)
    
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)

def delete_comment_view(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(post.comments, id=comment_id)
    comment.delete()
    
    referer = request.META.get('HTTP_REFERER')

    return redirect(referer)