from django.views import View
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from biblioteca.models import Course, User

class UserListView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'admin/list-users.html'
    
    def test_func(self):
        # Só permite se o usuário estiver no grupo "Bibliotecario"
        return self.request.user.groups.filter(name='Bibliotecario').exists()

    def handle_no_permission(self):
        from django.shortcuts import redirect
        # Redireciona se o usuário não tiver permissão (por grupo, por exemplo)
        return redirect('documents.custom')  # ou outra página como "sem_permissao"

    def get(self, request):
        users = User.objects.prefetch_related('groups').all()
        return render(request, self.template_name, {'users': users})
    
class CreateUserView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/register-user.html'
    
    @staticmethod  
    def generateDefaultPassword(last_name, phone):
        if not last_name or not phone:
            return None
        return f"{last_name.strip().capitalize()}{phone.strip()}"
    
    def test_func(self):
        # Só permite se o usuário estiver no grupo "Bibliotecario"
        return self.request.user.groups.filter(name='Bibliotecario').exists()

    def handle_no_permission(self):
        from django.shortcuts import redirect
        # Redireciona se o usuário não tiver permissão (por grupo, por exemplo)
        return redirect('documents.custom')  # ou outra página como "sem_permissao"

    def get(self, request):
        groups = Group.objects.all()
        courses = Course.objects.all()
        return render(request, self.template_name, {
            'groups': groups,
            'courses': courses
        })

    def post(self, request):
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        profile = request.POST.get('profile')
        phone = request.POST.get('phone')
        password = CreateUserView.generateDefaultPassword(last_name,phone)

        if User.objects.filter(username=email).exists():
            groups = Group.objects.all()
            courses = Course.objects.all()
            return render(request, self.template_name, {
                'erro': 'Usuário já existe.',
                'groups': groups,
                'courses': courses
            })

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email,
            phone = phone,
            password= password
        )

        if profile:
            try:
                group = Group.objects.get(name=profile)
                user.groups.add(group)
            except Group.DoesNotExist:
                pass

        user.save()
        messages.success(request, f"Usuário criado com sucesso! E-mail: {email} | Senha temporária: {password}")
        return redirect('users.successfully')

    
class CreatedSuccessfullUser(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'admin/created-successfully-user.html'
    
    def test_func(self):
        # Só permite se o usuário estiver no grupo "Bibliotecario"
        return self.request.user.groups.filter(name='Bibliotecario').exists()

    def handle_no_permission(self):
        return redirect('documents.custom')  # ou outra página como "sem_permissao"
    
    def get(self, request):
        return render(request, self.template_name)
    