from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import ItemForm
from .models import Item, List


def home_page(request):
    form = ItemForm()
    return render(request, 'home.html', {'form': form})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    return render(request, 'lists/list.html', {'list': list_, 'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})
