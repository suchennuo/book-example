from django import forms
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


