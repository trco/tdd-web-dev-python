from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    context = {}
    list_ = List.objects.get(id=list_id)
    context['list'] = list_

    return render(request, 'lists/list.html', context)


def new_list(request):
    # post request
    if request.method == 'POST':
        list_ = List.objects.create()
        Item.objects.create(text=request.POST.get('item_text'), list=list_)
        return redirect(f'/lists/{list_.id}/')

    return render(request, 'home.html')


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST.get('item_text'), list=list_)
    return redirect(f'/lists/{list_.id}/')
