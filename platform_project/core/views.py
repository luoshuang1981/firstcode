from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from .forms import PostForm

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login') # Redirect to login page after successful registration
    template_name = 'registration/register.html'

def home(request):
    return render(request, 'core/home.html')

class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'core/post_form.html'
    success_url = reverse_lazy('post_list') # Redirect to post list after successful post creation

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class PostListView(generic.ListView):
    model = Post
    template_name = 'core/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'core/post_detail.html'
    context_object_name = 'post'

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'core/post_form.html' # Reuse the creation form template

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        post = self.get_object()
        return post.created_by == self.request.user

    def form_valid(self, form):
        # created_by should not change on update, test_func handles authorization
        # form.instance.created_by = self.request.user
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'core/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return post.created_by == self.request.user
