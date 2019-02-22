from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Category, Kakeibo
# Create your views here.

class KakeiboListView(ListView):
  model = Kakeibo
  template_name = 'kakeibo/kakeibo_list.html'

  def queryset(self):
    return Kakeibo.objects.all()
