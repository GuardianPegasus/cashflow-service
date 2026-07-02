from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/get-categories/', views.get_categories, name='get_categories'),
    path('api/get-subcategories/', views.get_subcategories, name='get_subcategories'),
    path('directories/', views.manage_directories, name='manage_directories'),
    path('directories/add-status/', views.add_status, name='add_status'),
    path('directories/add-type/', views.add_type, name='add_type'),
    path('directories/add-category/', views.add_category, name='add_category'),
    path('directories/add-subcategory/', views.add_subcategory, name='add_subcategory'),
    path('directories/delete/<str:model_name>/<int:item_id>/', views.delete_directory_item, name='delete_directory_item'),
    path('record/edit/<int:record_id>/', views.edit_record, name='edit_record'),
    path('record/delete/<int:record_id>/', views.delete_record, name='delete_record'),
]