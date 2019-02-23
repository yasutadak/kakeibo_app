from django.urls import path
from . import views

app_name = 'kakeibo'

urlpatterns = [
  path('kakeibo_list/', views.KakeiboListView.as_view(), name='kakeibo_list'),
  ]
