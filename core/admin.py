from django.contrib import admin
from .models import Status, Type, Category, Subcategory, CashFlowRecord

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'income_expense_type')
    list_filter = ('income_expense_type',)
    search_fields = ('name',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(CashFlowRecord)
class CashFlowRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'income_expense_type', 'category', 'subcategory', 'status', 'comment')
    list_filter = ('date', 'income_expense_type', 'status', 'category')
    search_fields = ('comment', 'amount')
    ordering = ('-date', '-created_at')