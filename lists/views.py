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
            # Item.objects.create(text=request.POST['text'], list=list_)
            form.save(for_list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list':list_, "form": form, 'error':error})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        # Item.objects.create(text=request.POST['text'], list=list_)
        form.save(for_list=list_)
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



"""

从用户的请求中读取数据，结合一些定制的逻辑或 URL 中的信息 （list_id),
然后把数据传入表单验证，如果通过就保存数据， 最后重定向或者渲染模板

view 负责模板的重定向和渲染

    之前view 负责读取数据，验证，保存数据，重定向，渲染
    template 负责展示
    典型的 MVC 结构，但 C 模块过于繁重， 拆分出一个 form , 主要负责数据的处理
    包括读取，验证，存入数据库， 设置验证信息。这样，view 模板只负责提供将数据的转移给模板

model 负责数据库中数据的描述
form 负责读取数据，验证，保存数据
template 展示模板


"""