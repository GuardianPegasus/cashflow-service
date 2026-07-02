from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Status, Type, Category, Subcategory, CashFlowRecord

class CashFlowBusinessLogicTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.status = Status.objects.create(name="Бизнес")
        self.type_income = Type.objects.create(name="Пополнение")
        self.type_expense = Type.objects.create(name="Списание")
        
        self.category_marketing = Category.objects.create(
            name="Маркетинг", 
            income_expense_type=self.type_expense
        )
        self.subcategory_avito = Subcategory.objects.create(
            name="Avito", 
            category=self.category_marketing
        )

    def test_clean_method_raises_error_on_invalid_type_and_category(self):
        """Проверяем, что модель выкидывает ошибку, если категория не соответствует типу операции"""
        record = CashFlowRecord(
            date="2026-07-02",
            status=self.status,
            income_expense_type=self.type_income, # пополнение
            category=self.category_marketing, # но категория привязана к "Списанию"!
            subcategory=self.subcategory_avito,
            amount=5000.00
        )
        # full_clean() вызывает внутренний метод clean() модели
        with self.assertRaises(ValidationError):
            record.full_clean()

    def test_api_get_categories_returns_correct_json(self):
        """Проверяем, что API возвращает только категории, связанные с переданным типом"""
        url = reverse('get_categories')
        response = self.client.get(url, {'type_id': self.type_expense.id})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Маркетинг")