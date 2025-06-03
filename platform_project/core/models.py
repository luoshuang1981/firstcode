from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('supply', 'Supply'),
        ('demand', 'Demand'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

MEMBERSHIP_LEVEL_CHOICES = [
    ('free', 'Free'),
    ('bronze', 'Bronze'),
    ('silver', 'Silver'),
    ('gold', 'Gold'),
]

class Membership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=10, choices=MEMBERSHIP_LEVEL_CHOICES, default='free')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_level_display()}"
