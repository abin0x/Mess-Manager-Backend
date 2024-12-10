from django.contrib import admin
from .models import Mess,MembershipRequest
# Register your models here.
admin.site.register(MembershipRequest)
admin.site.register(Mess)