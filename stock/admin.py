from django.contrib import admin
from .models import User, Supplier, Product, StockMovement
# Register your models here.

# On enregistre notre modèle utilisateur personnalisé
admin.site.register(User)

# On enregistre les autres modèles de notre gestion de stock
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(StockMovement)
