from django.contrib import admin
from .models import Post, Comments, CommentsReplay, Tag


admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(CommentsReplay)
admin.site.register(Tag)
