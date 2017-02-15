from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from django.core.exceptions import ValidationError

from lists.forms import ItemForm


# Create your views here.
def home_page(request):
    # if request.method == 'POST':
    #     new_item_text = request.POST['text']
    #     Item.objects.create(text=new_item_text)
    #     return redirect('/lists/the-only-list-in-the-world/')

    # items = Item.objects.all()
    # return render(request, 'home.html', {'items':items})
    return render(request, 'home.html', {'form':ItemForm()})
    # else:
    #     new_item_text = ''

    # item = Item();
    # item.text = request.POST.get('text', '')
    # item.save()

    # return render(request, 'home.html',{
    #     # 'new_item_text':request.POST.get('text', ''),
    #     'new_item_text' : new_item_text,
    # })


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    # items = Item.objects.filter(list=list_)
    error = None
    list_ = List.objects.get(id=list_id)
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list':list_, "form": form, 'error':error})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form":form})
    # try:
    #     item.full_clean()
    #     item.save()
    # except ValidationError:
    #     list_.delete()
    #     error = "You can't have an empty list item"
    #     return render(request, 'home.html', {"error":error})
    # return redirect(list_)
