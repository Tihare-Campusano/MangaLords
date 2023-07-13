from django import forms
from .models import Manga, Contacto

class CrudForm(forms.ModelForm):

    class Meta:
        model = Manga
        fields = '__all__'
    

#parte deni
class ContactoForm(forms.ModelForm):
    
    class Meta:
        model = Contacto
        fields = '__all__'