from django.shortcuts import render
from . forms import KakeiboForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Category, Kakeibo
from kakeibo.models import Kakeibo
from django.db import models
from django.db.models import Sum
# Create your views here.

class KakeiboListView(ListView):
  model = Kakeibo
  template_name = 'kakeibo/kakeibo_list.html'

  def queryset(self):
    return Kakeibo.objects.all()

class KakeiboCreateView(CreateView):
  #利用するモデルを指定
  model = Kakeibo
  #利用するフォームクラス名を指定
  form_class = KakeiboForm
  #登録処理が正常終了した場合の遷移先を指定
  success_url = reverse_lazy('kakeibo:create_done')

def create_done(request):
  #登録処理が正常終了した場合に呼ばれるテンプレートを指定
  return render(request, 'kakeibo/create_done.html')
class KakeiboUpdateView(UpdateView):
  model = Kakeibo
  form_class = KakeiboForm
  success_url = reverse_lazy('kakeibo:update_done')

def update_done(request):
  return render(request, 'kakeibo/update_done.html')

class KakeiboDeleteView(DeleteView):
  model = Kakeibo
  success_url =reverse_lazy('kakeibo:delete_done')

def delete_done(request):
  return render(request, 'kakeibo/delete_done.html')


def show_circle_graph(request):
  kakeibo_data = Kakeibo.objects.all()

  total = 0
  for item in kakeibo_data:
      total += item.money

  category_list = []
  category_data = Category.objects.all()
  for item in category_data:
    category_list.append(item.category_name)

  category_dict = {}
  for i,item in enumerate(category_list):
    category_total = Kakeibo.objects.filter(category__category_name=category_list[i]).aggregate(sum=models.Sum('money'))['sum']
    if category_total != None:
      ratio = int((category_total / total) * 100)
      category_dict[item] = ratio
    else:
      ratio = 0
      category_dict[item] = ratio

  return render(request, 'kakeibo/kakeibo_circle.html',{'category_dict':category_dict})

def show_line_graph(request):
  kakeibo_data = Kakeibo.objects.all()

  category_list = []
  category_data = Category.objects.all().order_by('-category_name')
  for item in category_data:
    category_list.append(item.category_name)

  date_list = []
  for i in kakeibo_data:
    date_list.append((i.date.strftime('%Y/%m/%d')[:7]))
    date_list.sort()
    x_label = list(set(date_list))
    x_label.sort(reverse=False)

  #月毎&カテゴリ毎の合計金額データセットの生成
  monthly_sum_data = []
  for i in range(len(x_label)):
    year, month = x_label[i].split("/")
    #該当月の月末日を抽出
    month_range = calendar.monthrange(int(year), int(month))[1]
    first_date = year + '-' + month + '-' + '01'
    last_date = year + '-' + month + '-' + str(month_range)
    #1か月分のデータを取得
    total_of_month = Kakeibo.objects.filter(date__range=(first_date, last_date))
    category_total = total_of_month.values('category').annotate(total_price=Sum('money'))

    for j in range(len(category_total)):
      money = category_total[j]['total_price']
      category = Category.objects.get(pk=category_total[j]['category'])
      monthly_sum_data.append([x_label[i], category.category_name,money])
