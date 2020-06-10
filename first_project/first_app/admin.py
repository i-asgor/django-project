from django.contrib import admin
from first_app.models import AccessRecord, Topic, Webpages, Users, UserProfileInfo
# Register your models here.
admin.site.register(AccessRecord)
admin.site.register(Topic)
admin.site.register(Webpages)
admin.site.register(Users)
admin.site.register(UserProfileInfo)
