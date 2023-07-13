from django.shortcuts import render, redirect, redirect, get_object_or_404
from .models import Manga, RegistroUsuario
from .registroCli import registroClient
from django.contrib.auth import authenticate, login, logout
from .forms import CrudForm, ContactoForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def MangaLords(request):
    return render(request,'app/MangaLords.html')

def admin(request):
    return render(request,'app/admin.html')


def directorio(request):
    mangas = Manga.objects.all()
    return render(request,'app/directorio.html',{'mangas': mangas})

def inicioSecion(request):
    data = {
        'login': AuthenticationForm()
    }
    if request.method == 'POST':
        print(request.POST)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            print('Esta correcto')
            user = authenticate( request, username=username, password=password )
            login( request, user )
            return redirect('MangaLords')
        else:
            print('Incorrecto')
            
    return render(request,'app/inicioSecion.html', data)

def pagar(request):
    return render(request,'app/pagar.html')

@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('inicioSecion')

# aca se usa esto iregistroSecion
def Registro(request):
    data ={
        'registroCli' : registroClient()
    }
    if request.method == 'POST':
        print(request.POST)
        registroCli = registroClient(data=request.POST)
        if registroCli.is_valid():
            username = request.POST.get('email')
            password1 = request.POST.get('password1')
            nombre = request.POST.get('nombres')
            apellido = request.POST.get('apellidos')
            telefono = request.POST.get('telefono')
            
            user = User.objects.create_user(username, password=password1,
                    email=username, first_name=nombre, last_name=apellido)
            user.save()
            usuario = RegistroUsuario.objects.create(user= user, nombres=nombre, apellidos=apellido, email=username, telefono = telefono)
            usuario.save()
            # registroCli.save()
            print('Se guardo')
            # # user = authenticate(user_name=registroCli.cleaned_data['username'], password=registroCli.cleaned_data['password1'])
            login(request, user = user)
            
            return redirect('MangaLords')
        else:
            print(registroCli.errors)
    return render(request,'app/RegistroUsuario.html',data)


# contacto
def contacto(request):
    data = {
        'form': ContactoForm()
    }
    if request.method == 'POST':
        formulario = ContactoForm(data = request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Mensaje enviado"
        else:
            data["form"] = formulario
            
    return render(request,'app/contacto.html',data)


# leer datos de la clase creada
def vistaManga(request,pk):
    mangas = Manga.objects.get(id=pk)
    return render(request,'app/vistaManga.html',{'mangas': mangas})
    
    

# hecho por el make agregar listar modificar y eliminar
def agregar_producto(request):
    
    data = {
        'form': CrudForm()
    }

    if request.method == 'POST':
        print(request.POST, request.FILES)

        formulario = CrudForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Guardado correctamente"
        else:
            data["form"] = formulario

            print(formulario.errors)

    return render(request, 'app/crud/agregar.html', data)

def listar_productos(request):
    mangas = Manga.objects.all()

    data = {
        'mangas': mangas
    }

    return render(request, 'app/crud/listar.html', data)

def modificar_manga(request, id):

    manga = get_object_or_404(Manga, id=id)

    data = {
        'form': CrudForm(instance=manga)
    }

    if request.method == 'POST':
        formulario = CrudForm(data=request.POST, instance=manga, files=request.FILES)

        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_productos")
        data["form"] = formulario

    return render(request, 'app/crud/modificar.html', data)

def eliminar_producto(request, id):
    manga = get_object_or_404(Manga, id=id)
    manga.delete()
    return redirect(to="listar_productos")


def carrito(request):
    return render(request,'app/carrito.html')