from django.contrib import admin
from .models import Test

class TestAdmin(admin.ModelAdmin):
  list_display = ('tsid','name', 'epid', 'date')

admin.site.register(Test, TestAdmin)