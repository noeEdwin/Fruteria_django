from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Max

from fruteria_app.models import Empleado
from .forms import EmpleadoRegistrationForm 
from .forms import LoginForm

# Create your views here.
def home(request):
    return HttpResponse("Bienvenido a la Frutería")


def register_view(request):
    if request.method == "POST":
        form = EmpleadoRegistrationForm(request.POST)
        if form.is_valid():
            # Si is_valid() es True, todos los datos están limpios y validados
            # Accedemos a ellos con form.cleaned_data
            data = form.cleaned_data
            max_id = Empleado.objects.aggregate(Max('id_e'))['id_e__max'] or 0
            id_e = max_id + 1
        try:    
            user = Empleado.objects.create_user(
                username=data['username'],
                password=data['password'],
                nombre=data['nombre'],
                id_e=id_e,
                turno=data.get('turno'), 
                salario=data.get('salario')
            )
            login(request, user)
            messages.success(request, "¡Registro exitoso!")
            return redirect('home')
        except Exception as e:
                # El formulario es válido, pero falló la creación (error de DB, etc.)
                messages.error(request, f"Error inesperado al crear el usuario: {str(e)}")
    else:
        form = EmpleadoRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = Empleado.objects.get(username=username)
            if user and user.check_password(password):
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Credenciales inválidas.")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')