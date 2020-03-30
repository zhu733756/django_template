from django.contrib import admin
from .models import *

admin.site.register([UserInfo, TaskInfo,VideoInfo, XinhuaWeb])

# Register your models here.
