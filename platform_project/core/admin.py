from django.contrib import admin
from .models import Post, Category, Membership

# Register your models here.

class MembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'start_date', 'end_date']
    list_filter = ['level', 'start_date', 'end_date']
    search_fields = ['user__username']

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Membership, MembershipAdmin)
