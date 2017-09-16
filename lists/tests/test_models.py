from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.db import models
from django.core.exceptions import ValidationError
from unittest import skip
from lists.views import home_page
from lists.models import Item, List
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

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




class ListModeTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % (list_.id))

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()
            # item.save()

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()

        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()

    def test_lists_can_have_owners(self):
        user = User.objects.create(email='yongchao1122@126.com')
        list_ = List.objects.create(owner=user)
        self.assertIn(list_, user.list_set.all())

    def test_list_owner_is_optional(self):
        List.objects.create()


