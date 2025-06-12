from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Course

class CoursesView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'admin/courses.html'
    
    def test_func(self):
        # Só permite se o usuário estiver no grupo "Bibliotecario"
        return self.request.user.groups.filter(name='Bibliotecario').exists()

    def handle_no_permission(self):
        from django.shortcuts import redirect
        # Redireciona se o usuário não tiver permissão (por grupo, por exemplo)
        return redirect('documents.custom')  # ou outra página como "sem_permissao"

    def get(self, request): 
       courses = Course.objects.all()
       return render(request, self.template_name, {'courses':courses})
   
    def post(self, request):
        course_id = request.POST.get('course_id') 
        course_name = request.POST.get('course', '').strip()

        # Validação: campo vazio
        if not course_name:
            messages.error(request, "O nome do curso é obrigatório.")
            return redirect('courses')

        # Se for edição (course_id enviado)
        if course_id:
            try:
                course = Course.objects.get(id=course_id)

                # Validação: nome duplicado (exceto se for o mesmo curso)
                if Course.objects.filter(name__iexact=course_name).exclude(id=course_id).exists():
                    messages.error(request, "Já existe outro curso com esse nome.")
                    return redirect('courses')

                course.name = course_name
                course.save()
                messages.success(request, "Curso atualizado com sucesso.")
            except Course.DoesNotExist:
                messages.error(request, "Curso não encontrado.")
        else:
            # Criação
            if Course.objects.filter(name__iexact=course_name).exists():
                messages.error(request, "Já existe um curso com esse nome.")
                return redirect('courses')

            Course.objects.create(name=course_name)
            messages.success(request, "Curso criado com sucesso.")

        return redirect('courses')
    
class DeleteCourseView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'admin/confirm-delete-course.html'
    
    def test_func(self):
        # Só permite se o usuário estiver no grupo "Bibliotecario"
        return self.request.user.groups.filter(name='Bibliotecario').exists()

    def handle_no_permission(self):
        from django.shortcuts import redirect
        # Redireciona se o usuário não tiver permissão (por grupo, por exemplo)
        return redirect('documents.custom')  # ou outra página como "sem_permissao"
    
    def get(self, request, id):
        course = get_object_or_404(Course, id=id)
        return render(request, self.template_name, {'course':course})
    
    def post(self, request, id):
        course = get_object_or_404(Course, id=id)
        course.delete()
        return redirect('courses')
        
 