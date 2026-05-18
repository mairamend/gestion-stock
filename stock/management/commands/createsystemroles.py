from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from stock.models import Supplier, Product, StockMovement

class Command(BaseCommand):
    help = "Initialise les rôles du système (Magasinier, Responsable Stock) avec leurs permissions de base."

    def handle(self, *args, **options):
        # 1. Définition des rôles à créer
        role_permissions = {
            'Magasinier' : [StockMovement], 
            'Responsable Stock': [Product,Supplier]
        }

        for role_name ,model_list  in role_permissions.items():
            # Créer ou récupérer le groupe (rôle)
            group, created = Group.objects.get_or_create(name=role_name)
            # Vider les anciennes permissions du groupe pour repartir sur une base propre
            group.permissions.clear()
            for model in model_list:
               # Récupérer le ContentType du modèle (l'identifiant interne de Django pour ce modèle)
                content_type = ContentType.objects.get_for_model(model)
                # Récupérer les 4 permissions natives générées par Django (add, change, delete, view)
                permissions = Permission.objects.filter(content_type=content_type)
                # Ajouter ces permissions au groupe
                group.permissions.add(*permissions)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Rôle '{role_name}' créé avec ses permissions."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Rôle '{role_name}' mis à jour avec ses permissions."))     
        self.stdout.write(self.style.SUCCESS("Initialisation complète des rôles et des permissions effectuée !"))