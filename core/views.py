from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import CashFlowRecord, Category, Subcategory, Status, Type
from .forms import CashFlowRecordForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm

def index(request):
    """Главная страница: вывод записей с фильтрацией, пагинацией и обработка формы"""
    # Базовый QuerySet с оптимизацией запросов
    records_list = CashFlowRecord.objects.select_related(
        'status', 'income_expense_type', 'category', 'subcategory'
    ).all().order_by('-date', '-created_at')

    # Извлекаем параметры фильтрации из GET-запроса
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status_id = request.GET.get('status')
    type_id = request.GET.get('type')
    category_id = request.GET.get('category')

    # Динамически собираем условия фильтрации через Q-объекты
    filters = Q()
    if start_date:
        filters &= Q(date__gte=start_date)
    if end_date:
        filters &= Q(date__lte=end_date)
    if status_id:
        filters &= Q(status_id=status_id)
    if type_id:
        filters &= Q(income_expense_type_id=type_id)
    if category_id:
        filters &= Q(category_id=category_id)

    records_list = records_list.filter(filters)

    # Настраиваем пагинацию: по 5 записей на страницу
    paginator = Paginator(records_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Обработка формы создания (POST)
    if request.method == 'POST':
        form = CashFlowRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CashFlowRecordForm()

    # Данные для отрисовки фильтров в HTML
    context = {
        'page_obj': page_obj,
        'form': form,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
    }
    return render(request, 'core/index.html', context)

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