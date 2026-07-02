from django import forms
from .models import CashFlowRecord, Status, Type, Category, Subcategory

class BootstrapFormMixin:
    """Миксин, автоматически добавляющий класс form-control ко всем полям формы"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Сохраняем уже существующие классы, если они есть, или создаем новые
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()

class CashFlowRecordForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CashFlowRecord
        fields = ['date', 'status', 'income_expense_type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'income_expense_type': forms.Select(attrs={'id': 'id_income_expense_type'}),
            'category': forms.Select(attrs={'id': 'id_category'}),
            'subcategory': forms.Select(attrs={'id': 'id_subcategory'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Необязательный комментарий...'}),
        }

class StatusForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

class TypeForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']

class CategoryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'income_expense_type']

class SubcategoryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']