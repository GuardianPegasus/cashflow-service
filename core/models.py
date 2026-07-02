from django.db import models
from django.core.exceptions import ValidationError

class Status(models.Model):
    """Справочник статусов (Бизнес, Личное, Налог и т.д.)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Статус")

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name

class Type(models.Model):
    """Справочник типов (Пополнение, Списание)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Тип операции")

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

    def __str__(self):
        return self.name

class Category(models.Model):
    """Справочник категорий. Привязан к Типу операции"""
    name = models.CharField(max_length=100, verbose_name="Категория")
    income_expense_type = models.ForeignKey(
        Type, 
        on_delete=models.CASCADE, 
        related_name='categories', 
        verbose_name="Тип операции"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ('name', 'income_expense_type')

    def __str__(self):
        return f"{self.name} ({self.income_expense_type.name})"

class Subcategory(models.Model):
    """Справочник подкатегорий. Привязан к Категории"""
    name = models.CharField(max_length=100, verbose_name="Подкатегория")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='subcategories', 
        verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        unique_together = ('name', 'category')

    def __str__(self):
        return self.name

class CashFlowRecord(models.Model):
    """Основная таблица учета движения денежных средств (ДДС)"""
    date = models.DateField(verbose_name="Дата операции")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    income_expense_type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, verbose_name="Подкатегория")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма (руб.)")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")

    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
        ordering = ['-date', '-created_at']

    def clean(self):
        """Серверная валидация бизнес-правил ТЗ"""
        super().clean()
        
        # Проверяем, что выбранная категория жестко привязана к типу операции
        if hasattr(self, 'category') and hasattr(self, 'income_expense_type'):
            if self.category.income_expense_type != self.income_expense_type:
                raise ValidationError({
                    'category': f"Выбранная категория '{self.category.name}' не относится к типу '{self.income_expense_type.name}'."
                })
        
        # Проверяем, что выбранная подкатегория принадлежит выбранной категории
        if hasattr(self, 'subcategory') and hasattr(self, 'category'):
            if self.subcategory.category != self.category:
                raise ValidationError({
                    'subcategory': f"Выбранная подкатегория '{self.subcategory.name}' не принадлежит категории '{self.category.name}'."
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)