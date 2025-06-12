from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.views.generic import FormView

class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm # Usa o formulário de autenticação padrão do Django

    # O método 'get' é automaticamente tratado por FormView para exibir o formulário.
    # O método 'post' é automaticamente tratado por FormView para validar o formulário.

    def form_valid(self, form):
        # Este método é chamado quando o formulário é válido (usuário e senha corretos).
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)

            # Pega os grupos do usuário
            grupos = user.groups.values_list('name', flat=True)

            # Redireciona com base no grupo
            if 'Bibliotecario' in grupos:
                messages.success(self.request, f"Bem-vindo(a), {user.first_name}!")
                return redirect('admin_dashboard')
            elif 'Registo Academico' in grupos:
                messages.success(self.request, f"Bem-vindo(a), {user.first_name}!")
                return redirect('admin_dashboard')
            elif 'Estudante' in grupos:
                messages.success(self.request, f"Bem-vindo(a), {user.first_name}!")
                return redirect('documents.custom')
            elif 'Docente' in grupos:
                messages.success(self.request, f"Bem-vindo(a), {user.first_name}!")
                return redirect('documents.custom')
            
            # Fallback para usuários sem grupo específico ou caso nenhum match seja encontrado
            messages.success(self.request, f"Bem-vindo(a), {user.first_name}!")
            return redirect('default_dashboard') # Certifique-se de que esta URL existe

        else:
            # Isso não deve acontecer com AuthenticationForm, pois ele já valida as credenciais
            # antes de chamar form_valid. No entanto, é um fallback de segurança.
            messages.error(self.request, 'Credenciais inválidas. Verifique seu nome de usuário e senha.')
            return self.form_invalid(form) # Renderiza o formulário com erros se algo deu errado aqui
            
    def form_invalid(self, form):
        # Este método é chamado quando o formulário é inválido (usuário ou senha incorretos).
        # AuthenticationForm já adiciona os erros ao formulário.
        messages.error(self.request, 'Nome de usuário ou senha incorretos.')
        return super().form_invalid(form) # Renderiza o template com o formulário e os erros
