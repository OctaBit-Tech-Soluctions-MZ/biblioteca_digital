from .models import BlockedUser, Order, Document
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from core.decorators import is_logged, is_notLogged, group_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
@group_required('Estudante', 'Docente')
@is_logged
def home(request):
    documents = Document.objects.all()   
    return render(request, 'core/documents/list_doc_student.html', {'documents' : documents})

@group_required('Estudante', 'Docente')
@is_logged 
def profile():   
    return

@group_required('Estudante', 'Docente')
@is_logged 
def showDoc(request, id):
    document = get_object_or_404(Document, id=id)
    return render(request, 'core/documents/details_doc.html', {'document': document})

@group_required('Estudante', 'Docente')
@is_logged    
def printDoc(request, id):
    return

@group_required('Estudante', 'Docente')
@is_logged    
def downloadDoc():
    return

@is_notLogged
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Verifica o grupo do usuário
            if user.groups.filter(name='Admin').exists():
                return redirect('dashboard')
            elif user.groups.filter(name='docente').exists():
                return redirect('home')
            elif user.groups.filter(name='estudante').exists():
                return redirect('home')
            else:
                return redirect('home')  # ou uma página de acesso negado
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})