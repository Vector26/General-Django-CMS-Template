from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(PostContent)
admin.site.register(Likes)
admin.site.register(Comment)