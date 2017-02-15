from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from django.core.exceptions import ValidationError


# Create your views here.
def home_page(request):
    # if request.method == 'POST':
    #     new_item_text = request.POST['item_text']
    #     Item.objects.create(text=new_item_text)
    #     return redirect('/lists/the-only-list-in-the-world/')

    # items = Item.objects.all()
    # return render(request, 'home.html', {'items':items})
    return render(request, 'home.html')
    # else:
    #     new_item_text = ''

    # item = Item();
    # item.text = request.POST.get('item_text', '')
    # item.save()

    # return render(request, 'home.html',{
    #     # 'new_item_text':request.POST.get('item_text', ''),
    #     'new_item_text' : new_item_text,
    # })


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    # items = Item.objects.filter(list=list_)
    error = None

    if request.method == 'POST':
        try:
            item = Item.objects.create(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item"
    return render(request, 'list.html', {'list':list_,'error':error})


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error":error})
    return redirect(list_)
