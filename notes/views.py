from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from mainmenu.models import Profile

from .forms import EmailPostForm, PostForm
from .models import Post, Topic

import os
import configparser

"""
# Explanatory notes for the Owner views

 https://docs.djangoproject.com/en/3.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.ModelFormMixin.form_valid

 https://stackoverflow.com/questions/862522/django-populate-user-id-when-saving-a-model

 https://stackoverflow.com/a/15540149

 https://stackoverflow.com/questions/5531258/example-of-django-class-based-deleteview
"""


class OwnerListView(ListView):
    """
    Sub-class the ListView to pass the request to the form.
    """


class OwnerDetailView(DetailView):
    """
    Sub-class the DetailView to pass the request to the form.
    """


class OwnerCreateView(LoginRequiredMixin, CreateView):
    """
    Sub-class of the CreateView to automatically pass the Request to the Form
    and add the owner to the saved object.
    """

    # Saves the form instance, sets the current object for the view, and redirects to get_success_url().
    def form_valid(self, form):  # sourcery skip: avoid-builtin-shadow
        object = form.save(commit=False)
        object.owner = get_object_or_404(Profile, user=self.request.user)
        object.save()
        return super(OwnerCreateView, self).form_valid(form)


class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    """
    Sub-class the UpdateView to pass the request to the form and limit the
    queryset to the requesting user.
    """

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        qs = super(OwnerUpdateView, self).get_queryset()

        return qs.filter(owner=get_object_or_404(Profile, user=self.request.user))


class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other
    user's data.
    """

    def get_queryset(self):
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(owner=get_object_or_404(Profile, user=self.request.user))


def index(request):
    return render(request, 'notes/index.html')


class TopicListView(OwnerListView):
    model = Topic


class TopicDetailView(OwnerDetailView):
    model = Topic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['posts'] = context['topic'].post_set.all()

        if strval := self.request.GET.get("search", False):
            query = Q(title__icontains=strval)
            query.add(Q(body__icontains=strval), Q.OR)
            post_list = Post.objects.filter(
                query).select_related().order_by('-updated')[:10]
            context['posts'] = context['topic'].post_set.filter(
                query).select_related().order_by('-updated')[:10]
        else:
            context['posts'] = context['topic'].post_set.all()
        return context


@method_decorator(login_required, name='dispatch')
class TopicCreateView(OwnerCreateView):  # Convention: topic_form.html
    model = Topic
    fields = ['type', 'text']


@method_decorator(login_required, name='dispatch')
class TopicUpdateView(OwnerUpdateView):  # Convention: topic_form.html
    model = Topic
    fields = ['type', 'text']


@method_decorator(login_required, name='dispatch')
class TopicDeleteView(OwnerDeleteView):  # Convention: topic_confirm_delete.html
    model = Topic


class PostDetailView(OwnerDetailView):
    model = Post

    # NEW
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['references'] = context['post'].references.all()
        return context


@method_decorator(login_required, name='dispatch')
class PostCreateView(OwnerCreateView):  # Convention: post_form.html
    model = Post
    fields = ['title', 'body', 'status', 'url']

    def post(self, request, pk):
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = get_object_or_404(Profile, user=request.user)
            new_post.topic = get_object_or_404(Topic, id=pk)
            new_post.save()
            messages.success(request, ("Post Has Been Added"))
            return redirect(reverse('notes:topic_detail', args=[pk]))


@method_decorator(login_required, name='dispatch')
class PostUpdateView(OwnerUpdateView):  # Convention: post_form.html
    model = Post
    fields = ['title', 'body', 'status', 'url']

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        topic = post.topic
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Post Has Been Updated"))
            return redirect(reverse('notes:topic_detail', args=[topic.id]))


@method_decorator(login_required, name='dispatch')
# Convention: post_confirm_delete.html
class PostDeleteView(SuccessMessageMixin, OwnerDeleteView):
    model = Post
    # But returnes to topic list. How can we add the topic id to this.
    success_url = reverse_lazy('notes:topic_detail')
    success_message = "Post Has Been Deleted"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)


@login_required
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            cwd = os.getcwd()
            if cwd == '/app' or cwd[:4] == '/tmp':
                app_id = os.environ['EMAIL_ADDRESS']
            else:
                config = configparser.ConfigParser()
                config.read(os.path.join("D:\\Data", "API_Keys", "TPAMWeb.ini"))
                address = config['Email']['address']
            send_mail(subject, message, address, [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'notes/share.html', {'post': post, 'form': form, 'sent': sent})


def enamel_signs(request):
    return render(request, 'notes/enamel_signs.html')