from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(_("name"), max_length=100)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

class Post(models.Model):
    POST_TYPE_CHOICES = [
        (_('supply'), _('Supply')),
        (_('demand'), _('Demand')),
    ]

    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(_("description"))
    post_type = models.CharField(_("post type"), max_length=10, choices=POST_TYPE_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("created by"))
    categories = models.ManyToManyField(Category, verbose_name=_("categories"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['-created_at']

    def __str__(self):
        return self.title

MEMBERSHIP_LEVEL_CHOICES = [
    (_('free'), _('Free')),
    (_('bronze'), _('Bronze')),
    (_('silver'), _('Silver')),
    (_('gold'), _('Gold')),
]

class Membership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("user"))
    level = models.CharField(_("level"), max_length=10, choices=MEMBERSHIP_LEVEL_CHOICES, default='free')
    start_date = models.DateField(_("start date"), null=True, blank=True)
    end_date = models.DateField(_("end date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Membership")
        verbose_name_plural = _("Memberships")

    def __str__(self):
        return f"{self.user.username} - {self.get_level_display()}"
