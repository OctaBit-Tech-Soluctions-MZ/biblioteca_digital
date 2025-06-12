from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from biblioteca.models import User

class ProfileView(LoginRequiredMixin, View):
    template_name = 'profile.html'

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        return render(request, self.template_name, {'user': user})

    def post(self, request):
        user = request.user

        # Verifica se é atualização de perfil ou troca de senha
        if 'oldpassword' in request.POST:
            # Alteração de senha
            old_password = request.POST.get('oldpassword')
            new_password = request.POST.get('password')
            confirmation_password = request.POST.get('confirmation_password')

            if not user.check_password(old_password):
                messages.error(request, "Senha antiga incorreta.")
            elif new_password != confirmation_password:
                messages.error(request, "As novas senhas não coincidem.")
            elif len(new_password) < 6:
                messages.error(request, "A nova senha deve ter pelo menos 6 caracteres.")
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Mantém o login ativo
                messages.success(request, "Senha alterada com sucesso.")

        else:
            # Atualização de perfil
            first_name = request.POST.get('firstname', '').strip()
            last_name = request.POST.get('lastname', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()

            if not first_name or not last_name or not email or not phone:
                messages.error(request, "Preencha todos os campos.")
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.phone = phone
                user.save()
                messages.success(request, "Perfil atualizado com sucesso.")

        return redirect('profile')  # Certifique-se que 'profile' está definido no urls.py
