from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse  # ideal para pruebas

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #crea un register , el otro un login
from django.contrib.auth.models import User #guarda al usuario creado
from django.contrib.auth import login, logout, authenticate # el login mantiene la sesion iniciada en una cookie, una vez registrado - el logout quita la session de la cookie o biskuit, el authenticate permite logear aun usuario verficando q exista en la bd
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required # evita q un usuario anonimo pueda acceder a partes donde es necesario estar logeado

from .forms import TaskForm
from .models import Task

#timezone de django

from django.utils import timezone

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html' ,{
        'form' : UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:                           
            #registrar usuario
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form' : UserCreationForm,
                    'error': 'el usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form' : UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user= request.user, datecompleted__isnull = True) #el datecompleted... nos ayuda a filtar las tareas q ya estan completas de las q no   
    return render(request,'tasks.html',{'tasks' : tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull = False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks' : tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_tasks.html',{
            'form_task' : TaskForm
        })
    else:

        try:
            #forma 1, guardar datos por la clase
            '''
            Task.objects.create(titulo = request.POST['titulo'], descripcion= request.POST['descripcion'], important=('important' in request.POST), user = request.user)

            '''
            #forma 2, guardar datos por el formulario
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('/tasks')
        except ValueError:
            return render(request, 'create_tasks.html',{
            'form_task' : TaskForm,
            'error' : 'porfavor provee de datos validos'    
        })
@login_required
def task_detail(request, task_id):
    task= get_object_or_404(Task,pk=task_id, user = request.user) # esto filtra las tareas por usuario y el user = request.user, nos serciora de q el usuario solo accedera a las tareas q creo
    if request.method =='GET':
        
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task' : task, 'form':form})
    else:
        try:
            
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('/tasks/')
        except ValueError:
            return render(request, 'task_detail.html', {'task' : task, 'form':form, 'error': 'error al actualizar'})
@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('/tasks')

@login_required
def delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('/tasks')

        


@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
   if request.method == 'GET':
        return render(request ,'signin.html',{
        'login' : AuthenticationForm
    })
   else:
        user = authenticate(request, username = request.POST['username'], password=request.POST['password'])
        print(request.POST)
        if user is None:
            return render(request, 'signin.html',{
                'login' : AuthenticationForm,
                'error' : 'Usuario o contraseña incorrectos'
            })
        else: 
            login(request, user)
            return redirect('/tasks')


            
       

