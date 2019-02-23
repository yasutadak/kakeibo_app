from django.urls import path
from . import views

app_name = 'kakeibo'

urlpatterns = [
  path('kakeibo_list/', views.KakeiboListView.as_view(), name='kakeibo_list'),
  path('kakeibo_create/', views.KakeiboCreateView.as_view(), name='kakeibo_create'),
  path('create_done/', views.create_done, name='create_done'),
  path('update/<int:pk>/', views.KakeiboUpdateView.as_view(), name='kakeibo_update'),
  path('update_done/', views.update_done, name='update_done'),
  ]
