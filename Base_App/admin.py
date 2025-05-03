from django.contrib import admin
from Base_App.models import *
from .models import Delivery
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(ItemList)
admin.site.register(Items)
admin.site.register(AboutUs)
admin.site.register(Delivery)


