from django.contrib import admin
from .models import Profile

from .models import Profile,Skill, Message
# Register your models here.
admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Skill)
