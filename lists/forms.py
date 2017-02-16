from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item

# class ItemForm(forms.Form):
#     item_text = forms.CharField(
#         widget=forms.fields.TextInput(attrs={
#             'placeholder': 'Enter a to-do item',
#             'class':'form-control input-lg',
#         }),
#     )

"""
def modelform_factory(...)

Returns a ModelForm containing form fields for the given model.

``fields`` is an optional list of field names. If provided, only the named
fields will be included in the returned fields. If omitted or '__all__',
all fields will be used.

``exclude`` is an optional list of field names. If provided, the named
fields will be excluded from the returned fields, even if they are listed
in the ``fields`` argument.

``widgets`` is a dictionary of model field names mapped to a widget.

``localized_fields`` is a list of names of fields which should be localized.

``formfield_callback`` is a callable that takes a model field and returns
a form field.

``labels`` is a dictionary of model field names mapped to a label.

``help_texts`` is a dictionary of model field names mapped to a help text.

``error_messages`` is a dictionary of model field names mapped to a
dictionary of error messages.

``field_classes`` is a dictionary of model field names mapped to a form
field class.
"""

EMPTY_LIST_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"

class ItemForm(forms.models.ModelForm):

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

    class Meta:
        model = Item
        fields = ('text',)
        widgets = { # !!! ModelForm 提供 widgets 参数

            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_LIST_ERROR}
        }

class ExistingListItemForm(ItemForm):

    def save(self):
        return forms.models.ModelForm.save(self)


    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    """
    需要了解一下 django 内部机理 对模型验证 对表单验证
    Django 在 form 和 model 中都会调用 validation_unique()， 借助 instance 属性
    (form.instance = model) 在 form 的
    validation_unique() 中调用 model 的 validation_unique()
    why:
        必须调用 model 的 validation_unique() ?
    because:
        是否出现 IntegrityError 完全取决于完整性约束是否由数据库执行。
    Django 想把 models.py 中 unique_together 除了作为应用层约束之外，还想把它加入数据库中
    我们希望在尝试保存数据之前调用 is_valid, 注意到重复。而不是直到数据库执行层才给出警告（integrityError)
    解决步骤：
    1. form 首先要知道 哪个清单 以及 待办事项文本。 参考 ItemForm 的流程
    2. form 层验证
    3.
    """
    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text':[DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
