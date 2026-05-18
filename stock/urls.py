from django.urls import path 
from .views import ProductListView,DashboardView, ProductDetailView, SupplierListView,SupplierDeleteView,SupplierUpdateView,SupplierCreateView, ProductCreateView,SupplierDetailView,ProductUpdateView,ProductDeleteView,StockMovementCreateView,StockMovementListView


app_name =  'stock'

urlpatterns =  [
    path('', DashboardView.as_view(), name='dashboard'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/add/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('suppliers', SupplierListView.as_view() , name='supplier_list'),
    path('suppliers/add/', SupplierCreateView.as_view(), name='supplier_create'),
    path('supplier/<int:pk>/', SupplierDetailView.as_view(), name='supplier_detail'),
    path('suppliers/<int:pk>/edit/', SupplierUpdateView.as_view(), name='supplier_edit'),
    path('suppliers/<int:pk>/delete/',SupplierDeleteView.as_view(), name='supplier_delete'),
    path('movements/', StockMovementListView.as_view(), name='movement_list'),
    path('movements/add/', StockMovementCreateView.as_view(), name='movement_create'),
    
]