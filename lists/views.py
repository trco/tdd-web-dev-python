from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Item


def home_page(request):
    # post request
    if request.method == 'POST':
        Item.objects.create(text=request.POST.get('item_text'))
        return redirect('/lists/one-list/')

    return render(request, 'home.html')


def view_list(request):
    context = {}
    items = Item.objects.all()
    context['items'] = items

    return render(request, 'lists/list.html', context)
