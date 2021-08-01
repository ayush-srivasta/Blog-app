from django.contrib import admin
from .models import Blog,Category,Comments
# Register your models here.
admin.site.register(Blog)
admin.site.register(Comments)
admin.site.register(Category)