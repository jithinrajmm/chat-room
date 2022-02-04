from django.contrib import admin

from base.models import User,Room,Topic,Message

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(User)

# Register your models here.
