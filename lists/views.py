from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request):
    context = {}
    items = Item.objects.all()
    context['items'] = items

    return render(request, 'lists/list.html', context)


def new_list(request):
    # post request
    if request.method == 'POST':
        list_ = List.objects.create()
        Item.objects.create(text=request.POST.get('item_text'), list=list_)
        return redirect('/lists/one-list/')

    return render(request, 'home.html')
