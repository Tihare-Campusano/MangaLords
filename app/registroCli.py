from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import RegistroUsuario
from django.contrib.auth.hashers import make_password


class registroClient(UserCreationForm):
    
    nombres = forms.CharField(max_length=500)
    apellidos = forms.CharField(max_length=500)
    telefono = forms.IntegerField(max_value=999999999)
    email = forms.EmailField()
    
    class Meta:
        model = RegistroUsuario
        fields= ['nombres', 'apellidos','email','telefono']
        
