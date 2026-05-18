from django.db import models

from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Product, Supplier, StockMovement
from .forms import StockMovementForm
from django.db.models import Q
from django.db.models import Sum, F, Count
# Create your views here.

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'stock/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Total des produits uniques et des fournisseurs
        context['total_products'] = Product.objects.count()
        context['total_suppliers'] = Supplier.objects.count()
        
       
        total_value = Product.objects.annotate(
            product_value=F('quantity_in_stock') * F('price')
        ).aggregate(total=Sum('product_value'))['total']
        
        context['total_stock_value'] = total_value or 0
        
        # 3. Nombre de produits en alerte (stock bas)
        context['low_stock_count'] = Product.objects.filter(
            quantity_in_stock__lte=F('min_threshold')
        ).count()
        
        # 4. Les 5 derniers mouvements de stock (Activité récente)
        context['recent_movements'] = StockMovement.objects.select_related('product').all().order_by('-date')[:5]
        
        # 5. Les 5 produits les plus bas en stock (Alerte visuelle)
        context['critical_products'] = Product.objects.filter(
            quantity_in_stock__lte=F('min_threshold')
        ).order_by('quantity_in_stock')[:5]

        return context
    
    
class ProductListView(LoginRequiredMixin,ListView):
    
    model = Product
    template_name = 'stock/product_list.html'
    context_object_name = 'products'
    paginate_by = 5
    
    def get_queryset(self):
        queryset = Product.objects.all().order_by('name')
        supplier_id = self.request.GET.get('supplier')
        search_query = self.request.GET.get('q')
        if search_query :
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(reference__icontains=search_query)
            )
        if supplier_id:
            queryset = queryset.filter(supplier_id=supplier_id)
        
        stock_status = self.request.GET.get('status')
        if stock_status == 'low':
            queryset = queryset.filter(quantity_in_stock__lte=models.F('min_threshold'))
        elif stock_status == 'normal':
             queryset = queryset.filter(quantity_in_stock__gt=models.F('min_threshold'))   
        return queryset
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['low_stock_count'] = Product.objects.filter(
            quantity_in_stock__lte=models.F('min_threshold')
        ).count()
        context['suppliers'] = Supplier.objects.all().order_by('name')
        return context
        
    
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'stock/product_detail.html' 
    context_object_name = 'product'  

class ProductCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Product
    permission_required = 'stock.add_product'
    template_name = 'stock/product_form.html'
    # Les champs nécessaires pour créer un produit
    fields = ['name', 'reference', 'price', 'quantity_in_stock', 'min_threshold', 'supplier']
    success_url = reverse_lazy('stock:product_list')
    
class ProductUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Product
    permission_required = 'stock.change_product'
    # On réutilise EXACTEMENT le même fichier HTML
    template_name = 'stock/product_form.html'
    # Les champs que le responsable a le droit de modifier
    fields = ['name', 'reference', 'price', 'min_threshold', 'supplier']
    success_url = reverse_lazy('stock:product_list')

class ProductDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'stock.delete_product'
    template_name = 'stock/product_confirm_delete.html'
    success_url = reverse_lazy('stock:product_list')
        
class SupplierListView(LoginRequiredMixin,ListView):
    
    model = Supplier
    template_name = "stock/supplier_list.html"
    context_object_name = 'suppliers'
    paginate_by = 5
    
    def get_queryset(self):
        queryset =  Supplier.objects.all().order_by('name')
        search_query = self.request.GET.get('q')
        
        if search_query:
            queryset = queryset.filter( Q(name__icontains=search_query))
        return queryset
class SupplierDetailView(LoginRequiredMixin, DetailView) :
    model = Supplier
    template_name = 'stock/supplier_detail.html'
    context_object_name = 'supplier'
        
class SupplierCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Supplier
    permission_required = 'stock.add_supplier'
    template_name = 'stock/supplier_form.html'
    fields = ['name', 'phone', 'email', 'address']
    success_url = reverse_lazy('stock:supplier_list')
# Vue pour modifier un fournisseur
class SupplierUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Supplier
    permission_required = 'stock.change_supplier'
    fields = ['name', 'phone', 'email', 'address']  # Mets ici les vrais champs de ton modèle Supplier
    template_name = 'stock/supplier_form.html'      # Tu peux réutiliser le même template que l'ajout !
    success_url = reverse_lazy('stock:supplier_list')

# Vue pour supprimer un fournisseur
class SupplierDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Supplier
    permission_required = 'stock.delete_supplier'
    template_name = 'stock/supplier_confirm_delete.html'
    success_url = reverse_lazy('stock:supplier_list')
    
class StockMovementListView(LoginRequiredMixin,ListView):
    model = StockMovement
    template_name = 'stock/movement_list.html' 
    context_object_name = 'movements'
    paginate_by = 10
    
    def get_queryset(self):
        
        queryset = StockMovement.objects.select_related('product', 'user').all().order_by('-date')
        
        # 1. Filtrage par Type (IN / OUT)
        movement_type = self.request.GET.get('type')
        if movement_type in ['IN', 'OUT']:
            queryset = queryset.filter(movement_type=movement_type)

        # 2. Filtrage par Période (Date de début)
        date_debut = self.request.GET.get('date_debut')
        if date_debut:
            queryset = queryset.filter(date__date__gte=date_debut)

        # 3. Filtrage par Période (Date de fin)
        date_fin = self.request.GET.get('date_fin')
        if date_fin:
            queryset = queryset.filter(date__date__lte=date_fin)

        return queryset
class StockMovementCreateView(LoginRequiredMixin, CreateView):
    model = StockMovement
    form_class = StockMovementForm  # <-- 2. Associe le formulaire ici à la place de fields
    template_name = 'stock/movement_form.html'
    success_url = reverse_lazy('stock:product_list')

    def form_valid(self, form):
        # On associe toujours l'opérateur connecté automatiquement
        form.instance.user = self.request.user
        return super().form_valid(form)