from django.contrib import admin
from models import *

# Register your models here.
admin.site.register(Repository)
admin.site.register(Branch)
admin.site.register(Commit)
admin.site.register(Push)