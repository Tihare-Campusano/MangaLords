from django.shortcuts import render, redirect, get_object_or_404
from .models import Manga, RegistroUsuario
from .registroCli import registroClient
from django.contrib.auth import authenticate, login, logout
from .forms import CrudForm, ContactoForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
import random
import time


# Create your views here.
@login_required
def MangaLords(request):
    return render(request,'app/MangaLords.html')

def admin(request):
    return render(request,'app/admin.html')


def directorio(request):
    from django.db.models import Q
    query = request.GET.get('q', '').strip()
    if query:
        mangas = Manga.objects.filter(
            Q(titulo__icontains=query) | Q(editorial__icontains=query)
        )
    else:
        mangas = Manga.objects.all()
    return render(request,'app/directorio.html',{'mangas': mangas, 'query': query})

def inicioSecion(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            print('Esta correcto')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('MangaLords')
        else:
            print('Incorrecto')
            
    return render(request, 'app/inicioSecion.html', {'login': form})

def pagar(request):
    return render(request,'app/pagar.html')

@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('inicioSecion')

# aca se usa esto iregistroSecion
def Registro(request):
    form = registroClient()
    if request.method == 'POST':
        form = registroClient(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            nombre = form.cleaned_data.get('nombres')
            apellido = form.cleaned_data.get('apellidos')
            telefono = form.cleaned_data.get('telefono')
            
            # Verificar de forma segura si el email o el usuario ya existe
            if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
                form.add_error('email', 'Este correo electrónico ya está registrado.')
            else:
                user = User.objects.create_user(
                    username=email,
                    password=password1,
                    email=email,
                    first_name=nombre,
                    last_name=apellido
                )
                user.save()
                usuario = RegistroUsuario.objects.create(
                    user=user,
                    nombres=nombre,
                    apellidos=apellido,
                    email=email,
                    telefono=telefono
                )
                usuario.save()
                print('Se guardo')
                login(request, user=user)
                return redirect('MangaLords')
        else:
            print(form.errors)
            
    return render(request, 'app/RegistroUsuario.html', {'registroCli': form})


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


# ─── PASSWORD RESET OTP ────────────────────────────────────────────────────────

@require_POST
def request_password_reset(request):
    """Genera un código OTP de 6 dígitos y lo guarda en sesión."""
    email = request.POST.get('email', '').strip().lower()
    
    if not email:
        return JsonResponse({'success': False, 'error': 'Ingresa tu correo electrónico.'})
    
    # Verificar si el correo existe (filter evita MultipleObjectsReturned)
    user = User.objects.filter(email=email).first()
    if user is None:
        # Por seguridad, no revelamos si el correo existe o no
        return JsonResponse({'success': True, 'message': 'Si el correo existe, recibirás un código.'})
    
    # Generar OTP de 6 dígitos
    otp_code = str(random.randint(100000, 999999))
    otp_expiry = time.time() + getattr(settings, 'PASSWORD_RESET_OTP_EXPIRY', 600)
    
    # Guardar en sesión
    request.session['pwd_reset_otp'] = otp_code
    request.session['pwd_reset_otp_expiry'] = otp_expiry
    request.session['pwd_reset_email'] = email
    request.session.modified = True
    
    # Enviar correo (en desarrollo aparece en consola Y en el modal)
    try:
        send_mail(
            subject='🔐 MangaLords – Tu código de verificación',
            message=f'Tu código de verificación es: {otp_code}\n\nEste código expira en 10 minutos.\n\nSi no solicitaste esto, ignora este mensaje.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )
    except Exception:
        pass

    response_data = {'success': True, 'message': 'Si el correo existe, recibirás un código.'}

    # En modo DEBUG mostramos el código directamente (solo desarrollo)
    if settings.DEBUG:
        response_data['debug_code'] = otp_code

    return JsonResponse(response_data)


@require_POST
def verify_reset_code(request):
    """Verifica el código OTP ingresado por el usuario."""
    code = request.POST.get('code', '').strip()
    
    otp_code = request.session.get('pwd_reset_otp')
    otp_expiry = request.session.get('pwd_reset_otp_expiry', 0)
    
    if not otp_code:
        return JsonResponse({'success': False, 'error': 'No hay código pendiente. Solicita uno nuevo.'})
    
    if time.time() > otp_expiry:
        # Limpiar sesión expirada
        for key in ['pwd_reset_otp', 'pwd_reset_otp_expiry', 'pwd_reset_email']:
            request.session.pop(key, None)
        return JsonResponse({'success': False, 'error': 'El código ha expirado. Solicita uno nuevo.'})
    
    if code != otp_code:
        return JsonResponse({'success': False, 'error': 'Código incorrecto. Inténtalo de nuevo.'})
    
    # Marcar como verificado
    request.session['pwd_reset_verified'] = True
    request.session.modified = True
    return JsonResponse({'success': True})


@require_POST
def reset_password(request):
    """Actualiza la contraseña del usuario tras verificación OTP."""
    if not request.session.get('pwd_reset_verified'):
        return JsonResponse({'success': False, 'error': 'No autorizado. Verifica tu código primero.'})
    
    email = request.session.get('pwd_reset_email')
    password1 = request.POST.get('password1', '')
    password2 = request.POST.get('password2', '')
    
    if not password1 or len(password1) < 8:
        return JsonResponse({'success': False, 'error': 'La contraseña debe tener al menos 8 caracteres.'})
    
    if password1 != password2:
        return JsonResponse({'success': False, 'error': 'Las contraseñas no coinciden.'})
    
    user = User.objects.filter(email=email).first()
    if user is None:
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado.'})
    
    user.set_password(password1)
    user.save()
    
    # Limpiar sesión de reset
    for key in ['pwd_reset_otp', 'pwd_reset_otp_expiry', 'pwd_reset_email', 'pwd_reset_verified']:
        request.session.pop(key, None)
    
    return JsonResponse({'success': True, 'message': '¡Contraseña actualizada correctamente!'})


def search_suggestions(request):
    from django.http import JsonResponse
    from django.db.models import Q
    
    query = request.GET.get('q', '').strip()
    if len(query) >= 1:
        mangas = Manga.objects.filter(
            Q(titulo__icontains=query) | Q(editorial__icontains=query)
        )[:6]
        results = []
        for m in mangas:
            results.append({
                'id': m.id,
                'titulo': m.titulo,
                'editorial': m.editorial,
                'imagen_url': m.imagen.url if m.imagen else '',
            })
        return JsonResponse({'success': True, 'results': results})
    return JsonResponse({'success': True, 'results': []})