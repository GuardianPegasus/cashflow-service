from django import forms
from .models import CashFlowRecord, Status, Type, Category, Subcategory

class CashFlowRecordForm(forms.ModelForm):
    class Meta:
        model = CashFlowRecord
        fields = ['date', 'status', 'income_expense_type', 'category', 'subcategory', 'amount', 'comment']
        
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'income_expense_type': forms.Select(attrs={'class': 'form-control', 'id': 'id_income_expense_type'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'id_category'}),
            'subcategory': forms.Select(attrs={'class': 'form-control', 'id': 'id_subcategory'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Необязательный комментарий...'}),
        }

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'income_expense_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'income_expense_type': forms.Select(attrs={'class': 'form-control'}),
        }

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


from .models import Status, Type, Category, Subcategory
from .forms import StatusForm, TypeForm, CategoryForm, SubcategoryForm

def manage_directories(request):
    """Отображение страницы со всеми справочниками"""
    context = {
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.select_related('income_expense_type').all(),
        'subcategories': Subcategory.objects.select_related('category').all(),
        'status_form': StatusForm(),
        'type_form': TypeForm(),
        'category_form': CategoryForm(),
        'subcategory_form': SubcategoryForm(),
    }
    return render(request, 'core/manage_directories.html', context)

def add_status(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('manage_directories')

def add_type(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('manage_directories')

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('manage_directories')

def add_subcategory(request):
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('manage_directories')

def delete_directory_item(request, model_name, item_id):
    """Универсальное удаление элемента справочника"""
    models_mapping = {
        'status': Status,
        'type': Type,
        'category': Category,
        'subcategory': Subcategory
    }
    model = models_mapping.get(model_name)
    if model:
        try:
            item = model.objects.get(id=item_id)
            item.delete()
        except model.DoesNotExist:
            pass
    return redirect('manage_directories')