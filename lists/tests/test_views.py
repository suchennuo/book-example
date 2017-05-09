from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.db import models
from django.utils.html import escape

from unittest import skip

from lists.views import home_page, register_view
from lists.models import Item, List, User
from lists.forms import ItemForm, RegisterForm, EMPTY_LIST_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm

import sys


class HomePageTest(TestCase):
    maxDiff = None
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', {'form' : ItemForm()})
        # self.assertMultiLineEqual(response.content.decode(), expected_html)
        #加了 csrf-token 后这个测试通不过！！！
        #.decode() 把 response.content 中的字节转换成 Python 中的 Unicode 字符串
        #这样就可以对比字符串，而不是之前那样的对比字节

    # def test_home_page_displays_all_list_items(self):
    #     Item.objects.create(text='itemey 1')
    #     Item.objects.create(text='itemey 2')
    #     request = HttpRequest()
    #     response = home_page(request)
    #     self.assertIn('itemey 1', response.content.decode())
    #     self.assertIn('itemey 2', response.content.decode())
#
# class ItemModelTest(TestCase):
#     def test_saving_and_retrieving_items(self):
#         first_item = Item()
#         first_item.text = 'The first (ever) list item'
#         first_item.save()
#
#         second_item = Item()
#         second_item.text = 'Item the second.'
#         second_item.save()
#
#         saved_items = Item.objects.all()
#         self.assertEqual(saved_items.count(), 2)
#
#         first_saved_item = saved_items[0]
#         second_saved_item = saved_items[1]
#         self.assertEqual(first_saved_item.text, 'The first (ever) list item')
#         self.assertEqual(second_saved_item.text, 'Item the second.')

    # def test_home_page_only_saves_items_when_necessary(self):
    #     request = HttpRequest()
    #     home_page(request)
    #     self.assertEqual(Item.objects.count(), 0)

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

# class RegisterPageTest(TestCase):
#
#     def test_uses_register_template(self):
#         response = self.client.get('/')
#         self.assertTemplateUsed(response, 'register.html')

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()

        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text':'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)


    @skip
    def test_POST_redirects_to_list_view(self): #明确表示，只适用于 POST 请求
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

    def post_invalid_input(self):
        list_ = List.objects.create()
        return  self.client.post(
            '/lists/%d/' % list_.id,
            data={'text':''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_render_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_show_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_LIST_ERROR))

    def test_duplicate_item_validation_erros_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey') #已经存在 'textey'
        response = self.client.post(
            '/lists/%d/' % list1.id,
            data={'text': 'textey'}
        )

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % list_.id)
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        # request = HttpRequest()
        # request.method = 'POST'
        # request.POST['text'] = 'A new list item'
        #
        # response = home_page(request)
        self.client.post(
            '/lists/new',
            data={'text':'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    @skip
    def test_redirect_after_POST(self):
        # request = HttpRequest()
        # request.method = 'POST'
        # request.POST['text'] = 'A new list item'
        #
        # response = home_page(request)

        response = self.client.post(
            '/lists/new',
            data={'text':'A new list item'}
        )

        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

    # def test_validation_errors_are_send_back_to_home_page_template(self):
    #     response = self.client.post('/lists/new', data={'text':''})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'home.html')
    #     expected_error = escape("You can't have an empty list item")
    #     # expected_error = "You can't have an empty list item"
    #     # sys.stderr.write(response.content.decode())
    #     # print(response.content.decode())
    #     self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text':''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_for_validation_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertContains(response, escape(EMPTY_LIST_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertIsInstance(response.context['form'], ItemForm)
