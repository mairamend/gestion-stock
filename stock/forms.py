from django import forms
from .models import StockMovement , User



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # On ne met que les champs modifiables (Nom, Prénom, Photo)
        fields = ['first_name', 'last_name', 'photo_profil'] 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On applique le style Tailwind sur les champs texte
        for field_name, field in self.fields.items():
            if field_name != 'photo':  # On ne touche pas au style natif du champ fichier ici
                field.widget.attrs.update({
                    'class': 'form-input mt-1 block w-full rounded-xl border-night-200 text-sm'
                })
class StockMovementForm(forms.ModelForm):
  class Meta:
    model = StockMovement
    # Les champs qui apparaîtront dans le formulaire HTML
    fields = ['product', 'quantity', 'movement_type', 'description']

  def clean(self):
    """
    Cette méthode valide l'ensemble du formulaire.
    C'est ici qu'on ajoute notre sécurité anti-stock négatif.
    """
    cleaned_data = super().clean()
    product = cleaned_data.get('product')
    quantity = cleaned_data.get('quantity')
    movement_type = cleaned_data.get('movement_type')

    # Si c'est une sortie (OUT), on vérifie si on a assez de pièces en stock
    if movement_type == 'OUT' and product and quantity:
      if product.quantity_in_stock < quantity:
        # On lève une erreur de validation globale
        raise forms.ValidationError(
          f"Opération impossible ! Le stock actuel pour {product.name} est insuffisant "
          f"({product.quantity_in_stock} disponible(s), vous demandez d'en sortir {quantity})."
        )
        
    return cleaned_data