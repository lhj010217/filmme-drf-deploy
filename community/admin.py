from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Community, CommunityComment, CommunityImage, CommunityLike

admin.site.register(Community)
admin.site.register(CommunityComment)
admin.site.register(CommunityImage)
admin.site.register(CommunityLike)