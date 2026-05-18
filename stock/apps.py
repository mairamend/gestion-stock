from django.apps import AppConfig


class StockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stock'
    
    def ready(self):
        # Cette méthode est appelée quand Django démarre. 
        # On y importe nos signaux pour qu'ils soient actifs.
        import stock.signals
