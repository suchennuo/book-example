from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.db import models
from django.core.exceptions import ValidationError

from lists.views import home_page
from lists.models import Item, List

class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()


        second_item = Item()
        second_item.text = 'Item the second.'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second.')
        self.assertEqual(second_saved_item.list, list_)

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        #with 语句用于包装一段代码，这段代码往往用于设置，清理，处理错误
        #等价于
        # try:
        #     item.save()
        #     self.fail('The save should have raised an exception')
        # except ValidationError:
        #     pass
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
            # 测试本应该通过，TextField blank=False, 文本段本应该拒绝空值
            # Django 不会运行全部约束，在数据库中实现的约束， 保存数据时都会抛出异常
            # 但 SQLite 不支持文本字段上的强制控制约束，所以save() 方法通过了验证
            # Django 提供了一个用于全部验证的方法 full_clean()
