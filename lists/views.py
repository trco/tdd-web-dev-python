from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Item


def home_page(request):
    context = {}

    # post request
    if request.method == 'POST':
        Item.objects.create(text=request.POST.get('item_text'))
        return redirect('/')

    # get request
    items = Item.objects.all()
    context['items'] = items

    return render(request, 'home.html', context)
