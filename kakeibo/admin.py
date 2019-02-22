from django.contrib import admin
from .models import Category, Kakeibo
# Register your models here.

class KakeiboAdmin(admin.ModelAdmin):
  list_display=('date', 'category', 'money', 'memo')

admin.site.register(Category)
admin.site.register(Kakeibo, KakeiboAdmin)
