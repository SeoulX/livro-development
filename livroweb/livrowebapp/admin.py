from django.contrib import admin
from .models import *

admin.site.register(Member)
admin.site.register(Library)
admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(UserFave)