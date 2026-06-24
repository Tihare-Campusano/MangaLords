import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import RegistroUsuario

class registroClient(UserCreationForm):
    nombres = forms.CharField(
        max_length=100, 
        required=True, 
        label="Nombres",
        widget=forms.TextInput(attrs={'class': 'formulario__input', 'placeholder': 'Juan'})
    )
    apellidos = forms.CharField(
        max_length=100, 
        required=True, 
        label="Apellidos",
        widget=forms.TextInput(attrs={'class': 'formulario__input', 'placeholder': 'Pérez'})
    )
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'formulario__input',
            'placeholder': 'Ej: 987654321',
            'maxlength': '9',
            'pattern': '[0-9]{9}',
            'inputmode': 'numeric'
        }),
        label="Teléfono"
    )
    email = forms.EmailField(
        required=True, 
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'formulario__input', 'placeholder': 'juan.perez@correo.com'})
    )
    
    class Meta:
        model = RegistroUsuario
        fields = ['nombres', 'apellidos', 'email', 'telefono']
        
    def clean_nombres(self):
        nombres = self.cleaned_data.get('nombres')
        if nombres:
            nombres = nombres.strip()
            if len(nombres) < 2:
                raise forms.ValidationError("Los nombres deben tener al menos 2 caracteres.")
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombres):
                raise forms.ValidationError("Los nombres solo deben contener letras y espacios.")
        return nombres

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if apellidos:
            apellidos = apellidos.strip()
            if len(apellidos) < 2:
                raise forms.ValidationError("Los apellidos deben tener al menos 2 caracteres.")
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellidos):
                raise forms.ValidationError("Los apellidos solo deben contener letras y espacios.")
        return apellidos

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()
            # Validar si el email ya existe en User o RegistroUsuario
            if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
                raise forms.ValidationError("Este correo electrónico ya está registrado.")
            if RegistroUsuario.objects.filter(email=email).exists():
                raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email
        
    def clean_telefono(self):
        telefono_raw = self.cleaned_data.get('telefono')
        if not telefono_raw:
            raise forms.ValidationError("Este campo es obligatorio.")
        
        telefono_cleaned = str(telefono_raw).strip()
        
        if not telefono_cleaned.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números, sin símbolos ni letras.")
            
        if len(telefono_cleaned) != 9:
            raise forms.ValidationError("El teléfono debe tener exactamente 9 números (ej: 987654321).")
            
        return int(telefono_cleaned)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1:
            if len(password1) < 8:
                self.add_error('password1', "La contraseña debe tener al menos 8 caracteres.")
            elif not re.search(r"[a-z]", password1):
                self.add_error('password1', "La contraseña debe contener al menos una letra minúscula.")
            elif not re.search(r"[A-Z]", password1):
                self.add_error('password1', "La contraseña debe contener al menos una letra mayúscula.")
            elif not re.search(r"[0-9]", password1):
                self.add_error('password1', "La contraseña debe contener al menos un número.")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Las contraseñas no coinciden.")

        return cleaned_data
