from django.shortcuts import render, redirect, get_object_or_404
from core.models import BlockedUser, Order, Document
from django.utils.text import slugify
import random
from core.decorators import is_logged
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

# Create your views here.
@is_logged
def admin_dashboard(request):
    return render(request, 'dashboard.html')
@is_logged
def listUser(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users' : users})
@is_logged
def registerUser(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        perfil = request.POST.get('perfil')

        if User.objects.filter(username=email).exists():
            # Já existe usuário
            return render(request, 'create-user.html', {'erro': 'Usuário já existe.'})

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email,
            password='IDEM2025'
        )

        # Adiciona o usuário ao grupo
        if perfil:
            try:
                grupo = Group.objects.get(name=perfil)
                user.groups.add(grupo)
            except Group.DoesNotExist:
                pass  # Ou crie o grupo, se desejar

        user.save()

        return redirect('users')

    return render(request, 'create-user.html')
@is_logged
def generate_password():
    """Gera uma senha no formato 'idem1234'."""
    return 'idem' + str(random.randint(1000, 9999))
@is_logged
def recoverPassword(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        new_password = generate_password()
        user.set_password(new_password)
        user.save()

        return render(request, 'users/password_updated.html', {
            'user': user,
            'new_password': new_password
        })

    return render(request, 'users/recover_password.html', {'user': user})

@is_logged
def blockedUser(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        reason = request.POST.get('reason')
        BlockedUser.objects.create(user=user, reason=reason)
        return redirect('users') 

    return render(request, 'users.html', {'user': user})
@is_logged
def acceptOrder(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        order.status = 'aprovado'
        order.save()
        return redirect('orders')
    return redirect('orders') 
@is_logged
def listOrder(request):
    orders = Order.objects.all()
    return render(request, 'orders.html', {'orders' : orders})
def rejectOrder(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        order.status = 'rejeitado'
        order.save()
        return redirect('orders')
    return redirect('orders')
@is_logged
def reverterOrder(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        order.status = 'pendente'
        order.save()
        return redirect('orders')
    return redirect('orders')
@is_logged
def listDocument(request):
    documents = Document.objects.all()
    return render(request, 'documents.html', {'documents' : documents})

@is_logged
def registerDocument(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        year = request.POST.get('year')
        doc_type = request.POST.get('type')
        upload = request.FILES.get('upload')

        Document.objects.create(
            title=title,
            author=author,
            year=year,
            link=upload,
            slug=slugify(title),
            type=doc_type,
            score=0
        )
        return redirect('documents')

    return render(request, 'register_doc.html')
@is_logged
def editDocument(request, id):
    document = get_object_or_404(Document, id=id)

    if request.method == 'POST':
        document.title = request.POST.get('title')
        document.author = request.POST.get('author')
        document.year = request.POST.get('year')
        document.link = request.POST.get('upload')
        document.slug = slugify(document.title)
        document.save()

        return redirect('documents')

    return render(request, 'documents/edit.html', {'document': document})
@is_logged
def deleteDocument(request, id):
    document = get_object_or_404(Document, id=id)

    if request.method == 'POST':
        document.delete()
        return redirect('documents')

    return render(request, 'documents/delete_confirm.html', {'document': document})