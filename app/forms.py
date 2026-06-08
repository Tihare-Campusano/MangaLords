from django import forms
from .models import Manga, Contacto

class CrudForm(forms.ModelForm):

    class Meta:
        model = Manga
        fields = '__all__'
    

#parte deni
class ContactoForm(forms.ModelForm):
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'formulario__input',
            'placeholder': 'Ej: 987687678',
            'maxlength': '9',
            'pattern': '[0-9]{9}',
            'inputmode': 'numeric'
        }),
        label="Teléfono"
    )
    
    class Meta:
        model = Contacto
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'formulario__input', 'placeholder': 'Ingresa tu nombre'}),
            'email': forms.EmailInput(attrs={'class': 'formulario__input', 'placeholder': 'ejemplo@correo.com'}),
            'tipo_consulta': forms.Select(attrs={'class': 'formulario__input'}),
            'mensaje': forms.Textarea(attrs={'class': 'formulario__input', 'rows': 4, 'placeholder': 'Escribe tu mensaje aquí...'}),
        }

    def clean_telefono(self):
        telefono_raw = self.cleaned_data.get('telefono')
        if not telefono_raw:
            raise forms.ValidationError("Este campo es obligatorio.")
        
        telefono_cleaned = telefono_raw.strip()
        
        if not telefono_cleaned.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números, sin símbolos ni letras.")
            
        if len(telefono_cleaned) != 9:
            raise forms.ValidationError("El teléfono debe tener exactamente 9 números (ej: 987687678).")
            
        return int(telefono_cleaned)