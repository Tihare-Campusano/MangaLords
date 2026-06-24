from django import forms
from django.contrib.auth.models import User
from .models import Manga, Contacto, RegistroUsuario

class CrudForm(forms.ModelForm):

    class Meta:
        model = Manga
        fields = '__all__'
        widgets = {
            'id': forms.TextInput(attrs={
                'class': 'formulario__input', 
                'placeholder': 'Ej: MNG001', 
                'maxlength': '6',
                'pattern': '[a-zA-Z0-9]{1,6}'
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'formulario__input', 
                'placeholder': 'Título del Manga (Ej: Berserk Vol. 1)'
            }),
            'editorial': forms.TextInput(attrs={
                'class': 'formulario__input', 
                'placeholder': 'Editorial (Ej: Panini, Ivrea)'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'formulario__input', 
                'placeholder': 'Precio en CLP (Ej: 9990)',
                'min': '0'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'formulario__input', 
                'placeholder': 'Descripción detallada del manga...', 
                'rows': 4
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'formulario__input', 
                'placeholder': 'Stock disponible (Ej: 15)',
                'min': '0'
            }),
            'descuento': forms.NumberInput(attrs={
                'class': 'formulario__input',
                'placeholder': 'Descuento en % (Ej: 20)',
                'min': '0',
                'max': '100'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control-file text-white-50 mt-1',
                'accept': 'image/*'
            }),
        }

    

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
        exclude = ['user', 'respuesta', 'respondido', 'fecha_creacion', 'fecha_respuesta']
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


class PerfilForm(forms.ModelForm):
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
        model = RegistroUsuario
        fields = ['nombres', 'apellidos', 'email', 'telefono']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'formulario__input', 'placeholder': 'Nombres'}),
            'apellidos': forms.TextInput(attrs={'class': 'formulario__input', 'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'formulario__input', 'placeholder': 'ejemplo@correo.com'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_telefono(self):
        telefono_raw = self.cleaned_data.get('telefono')
        if not telefono_raw:
            raise forms.ValidationError("Este campo es obligatorio.")
        
        telefono_cleaned = str(telefono_raw).strip()
        
        if not telefono_cleaned.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números, sin símbolos ni letras.")
            
        if len(telefono_cleaned) != 9:
            raise forms.ValidationError("El teléfono debe tener exactamente 9 números (ej: 987687678).")
            
        return int(telefono_cleaned)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()
            qs = User.objects.filter(email=email)
            if self.user:
                qs = qs.exclude(pk=self.user.pk)
            if qs.exists():
                raise forms.ValidationError("Este correo electrónico ya está registrado por otro usuario.")
        return email