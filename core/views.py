from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import CashFlowRecord, Category, Subcategory, Status, Type
from .forms import CashFlowRecordForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm

def index(request):
    """Главная страница: вывод записей и обработка формы"""
    
    # Используем select_related для предотвращения проблемы запросов N+1
    records = CashFlowRecord.objects.select_related('status', 'income_expense_type', 'category', 'subcategory').all()
    
    if request.method == 'POST':
        form = CashFlowRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CashFlowRecordForm()
        
    return render(request, 'core/index.html', {
        'records': records,
        'form': form
    })

def get_categories(request):
    """Возвращает JSON с категориями для выбранного типа операции"""
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(income_expense_type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)

def get_subcategories(request):
    """Возвращает JSON с подкатегориями для выбранной категории"""
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

def edit_record(request, record_id):
    """Редактирование существующей записи ДДС"""
    try:
        record = CashFlowRecord.objects.get(id=record_id)
    except CashFlowRecord.DoesNotExist:
        return redirect('index')

    if request.method == 'POST':
        form = CashFlowRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CashFlowRecordForm(instance=record)

    return render(request, 'core/edit_record.html', {
        'form': form,
        'record': record
    })

def delete_record(request, record_id):
    """Удаление записи ДДС"""
    try:
        record = CashFlowRecord.objects.get(id=record_id)
        record.delete()
    except CashFlowRecord.DoesNotExist:
        pass
    return redirect('index')

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