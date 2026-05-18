from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email :
            raise ValueError("L'adresse email est obligatoire")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active',True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email,password,**extra_fields)
    
class User(AbstractUser):
    # On supprime le champ username natif de Django
    username = None
    
    # On définit l'email comme l'identifier unique
    email = models.EmailField('Adresse email0', unique=True)
    
        # Champs spécifique demandés 
    adresse = models.TextField('Adresse', blank = True, null = True )    
    date_naissance = models.DateField('Date de naissance', blank=True, null=True)
    photo_profil = models.ImageField('Photo de profil', upload_to='profiles/', blank=True, null=True)
    
    # On configure l'email pour l'utiliser comme identifiant
    
    USERNAME_FIELD =  'email' 
    REQUIRED_FIELDS =   ['first_name', 'last_name']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email


#   --- MODÈLE FOURNISSEUR ---

class Supplier(models.Model):
    
    name = models.CharField('Nom du fournisseur', max_length=150, unique=True)
    email = models.EmailField('Email du fournisseur',blank=True, null=True)
    phone = models.CharField('Téléphone', max_length=20, blank=True, null=True)
    address = models.TextField('Adresse', blank=True, null=True)
    
    def __str__(self):
        return self.name

  # --- MODÈLE PRODUIT ---
class Product(models.Model):
    name = models.CharField('Nom du produit', max_length=150)
    reference = models.CharField('Référence unique', max_length=50, unique=True)
    price = models.DecimalField('Prix unitaire', max_digits=10, decimal_places=2)
    quantity_in_stock = models.IntegerField('Quantité en stock', default=0)   
    min_threshold = models.IntegerField('Seuil d\'alerte stock bas', default=5)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products', verbose_name='Fournisseur')
    
    def __str__(self):
        return f"{self.name} ({self.reference})"
    
    #  Methode pour verifier si le stock est bas
    def is_low_stock(self):
        return self.quantity_in_stock <= self.min_threshold
    
   # --- MODÈLE MOUVEMENT DE STOCK ---

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Entrée (Arrivage/Retour)'),
        ('OUT', 'Sortie (Vente/Perte)'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements', verbose_name='Produit')
    quantity = models.PositiveIntegerField('Quantité transférée')
    movement_type = models.CharField('Type de mouvement', max_length=3, choices=MOVEMENT_TYPES)
    date = models.DateTimeField('Date du mouvement', auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Opérateur')
    description = models.TextField('Notes / Justification', blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.quantity}x {self.product.name}"