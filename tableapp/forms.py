from django import forms
from .models import Menu, Category, Item

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['menu_name', 'menu_url', 'image_field']
        widgets = {
            'menu_url': forms.TextInput(attrs={
                'id': 'menu_url_input',
                'placeholder': '/onlylettersordigits/',
                'pattern': '^/[a-zA-Z0-9]+/$',
                'title': 'Must start and end with / and contain only letters or digits'
            }),
        }

        labels = {
            'menu_name': 'Menu name',
            'menu_url': 'Short name in url',
            'image_field': 'Upload image'
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'category_url', 'category_image']
        widgets = {
            'category_url': forms.TextInput(attrs={
                'id': 'menu_url_input',
                'placeholder': '/onlylettersordigits/',
                'pattern': '^/[a-zA-Z0-9]+/$',
                'title': 'Must start and end with / and contain only letters or digits'
            }),
        }

        labels = {
            'menu_name': 'Category name',
            'menu_url': 'Short name in url',
            'image_field': 'Upload image'
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_image', 'description','pricing']
        labels = {
            'pricing': 'Pricing',
            'description': 'Description',
            'item_image': 'Upload Item Image',
            'item_name':'Item Name'
        }
        widgets = {
            'item_name': forms.TextInput(attrs={
                'id': 'name',
                'name': 'name',
                'required': True,
                'placeholder': 'Item Name',
                'style': (
                    'border: 2px solid var(--backgroundcolor);'
                    'width: 100%;'
                    'height: 35px;'
                    'background-color: #e9e5e5;'
                    'border-radius: 5px;'
                    'padding-left: 10px;'
                    'margin-bottom: 15px;'
                )
            }),
            'pricing': forms.TextInput(attrs={
                'id': 'pricing',
                'name': 'pricing',
                'required': True,
                'placeholder': 'Only Digits',
                'style': (
                    'border: 2px solid var(--backgroundcolor);'
                    'width: 100%;'
                    'height: 35px;'
                    'background-color: #e9e5e5;'
                    'border-radius: 5px;'
                    'padding-left: 10px;'
                    'margin-bottom: 15px;'
                )
            }),
            'description': forms.Textarea(attrs={
                'id': 'description',
                'name': 'description',
                'rows': 4,
                'required': True,
                'style': (
                    'width: 100%;'
                    'background-color: #e9e5e5;'
                    'border-radius: 5px;'
                    'padding: 10px;'
                    'border: 2px solid var(--backgroundcolor);'
                    'font-family: Montserrat, sans-serif;'
                    'margin-bottom: 15px;'
                    'resize: vertical;'
                )
            }),
            'item_image': forms.ClearableFileInput(attrs={
                'id': 'image',
                'name': 'image',
                'accept': 'image/*',
                'required': True,
                'style': (
                    'margin-bottom: 4px;'
                    'margin-top: 4px;'
                    'border: 1px solid #ccc;'
                    'border-radius: 10px;'
                    'display: inline-block;'
                    'padding: 6px 12px;'
                    'cursor: pointer;'
                )
            }),
        }