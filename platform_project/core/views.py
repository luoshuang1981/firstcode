from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _ # Add this import
from .models import Post
from .forms import PostForm

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        messages.success(self.request, _('Account created for {username}! You can now log in.').format(username=username))
        return response

def home(request):
    recent_posts = Post.objects.order_by('-created_at')[:3] # Get latest 3 posts
    context = {
        'recent_posts': recent_posts
    }
    return render(request, 'core/home.html', context)

class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'core/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, _("Post created successfully!"))
        return response

class PostListView(generic.ListView):
    model = Post
    template_name = 'core/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10 # Add pagination

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
        response = super().form_valid(form)
        messages.success(self.request, _("Post updated successfully!"))
        return response

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'core/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return post.created_by == self.request.user

    def form_valid(self, form):
        messages.success(self.request, _("Post '{title}' deleted successfully!").format(title=self.object.title))
        return super().form_valid(form)
