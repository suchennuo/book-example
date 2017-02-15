from django.test import TestCase
from lists.forms import ItemForm
from lists.forms import EMPTY_LIST_ERROR

class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = ItemForm()
        # self.fail(form.as_p()
        # 探索性编程，看 输出的 form 缺哪些属性，然后用 meta widget attrs= 等 API 补上
        # 为了让下面正经的 测试用例 通过

    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_LIST_ERROR]
        )