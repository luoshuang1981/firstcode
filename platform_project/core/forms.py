from django import forms
from .models import Post
from django.utils.translation import gettext_lazy as _

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'post_type', 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple,
        }
