from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StockMovement


@receiver(post_save, sender=StockMovement)
def update_product_stock(sender,instance,created, **kwargs):
    
    """
    Ce signal s'exécute AUTOMATIQUEMENT après chaque enregistrement 
    d'un mouvement de stock (StockMovement) en base de données.
    """
    
    if created :
        product = instance.product
        
        if instance.movement_type == 'IN':
            # Si c'est une entrée, on ajoute la quantité au stock du produit
            product.quantity_in_stock += instance.quantity
        elif instance.movement_type == 'OUT':
            # Si c'est une sortie, on soustrait la quantité du stock du produit
            product.quantity_in_stock -= instance.quantity
        
        # On sauvegarde le produit avec sa nouvelle quantité calculée
        product.save()    
                