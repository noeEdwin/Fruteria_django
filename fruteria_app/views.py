from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib import messages

from fruteria_app.models import Empleado
# Create your views here.
def home(request):
    return HttpResponse("Bienvenido a la Frutería")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        nombre = request.POST.get('nombre')
        id_e = request.POST.get('id_e')
        turno = request.POST.get('turno')
        salario = request.POST.get('salario')

        if not (username and password and confirm_password and nombre and id_e):
            messages.error(request, "Todos los campos obligatorios deben llenarse.")
            return render(request, 'registration/register.html')

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'registration/register.html')

        try:
            user = Empleado.objects.create_user(
                username=username,
                password=password,
                nombre=nombre,
                id_e=id_e,
                turno=turno,
                salario=salario
            )
            login(request, user)
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Error al registrar: {str(e)}")
    return render(request, 'registration/register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = Empleado.objects.filter(username=username).first()
        if user and user.check_password(password):
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Credenciales inválidas.")
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')