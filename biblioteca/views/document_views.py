from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from biblioteca.models import Course, Document, Order, AcessDocStatistic, DocumentGroup
from django.contrib.auth.models import Group

class ListDocuments(LoginRequiredMixin,UserPassesTestMixin, View):
    template_name = "admin/list-documents.html"
    
    def test_func(self):
        # Só permite se o usuário estiver no grupo "Bibliotecario"
        return self.request.user.groups.filter(name='Bibliotecario').exists()

    def handle_no_permission(self):
        from django.shortcuts import redirect
        # Redireciona se o usuário não tiver permissão (por grupo, por exemplo)
        return redirect('documents.custom')  # ou outra página como "sem_permissao"
    
    def get(self, request):
        documents = Document.objects.select_related('course').all()
        return render(request, self.template_name, {'documents':documents})

class DocumentCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'admin/register-documents.html'
    
    def test_func(self):
        # Só permite se o usuário estiver no grupo "Bibliotecario"
        return self.request.user.groups.filter(name='Bibliotecario').exists()

    def handle_no_permission(self):
        from django.shortcuts import redirect
        # Redireciona se o usuário não tiver permissão (por grupo, por exemplo)
        return redirect('documents.custom')  # ou outra página como "sem_permissao"

    def get(self, request):
        courses = Course.objects.all()
        groups = Group.objects.all()
        return render(request, self.template_name, {'courses': courses, 'groups':groups})

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        author = request.POST.get('author')
        year = request.POST.get('year')
        doc_type = request.POST.get('type')
        link = request.FILES.get('link')
        course = request.POST.get('course')
        selected_groups = request.POST.getlist('groups')

        document = Document.objects.create(
            title=title,
            author=author,
            description=description,
            year=year,
            link=link,
            slug=slugify(title),
            type=doc_type,
            score=0,
            course_id=course
        )
        print(selected_groups)
        if 'all' in selected_groups:
            groups = Group.objects.all()
        else:
            groups = Group.objects.filter(id__in=selected_groups)
        # Cria as permissões (relações) entre grupos e documento
        for group in groups:
            DocumentGroup.objects.create(
                group=group,
                document=document
            )
        return redirect('documents')
    
class DocumentUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'admin/edit-document.html'
    
    def test_func(self):
        # Só permite se o usuário estiver no grupo "Bibliotecario"
        return self.request.user.groups.filter(name='Bibliotecario').exists()

    def handle_no_permission(self):
        from django.shortcuts import redirect
        # Redireciona se o usuário não tiver permissão (por grupo, por exemplo)
        return redirect('documents.custom')  # ou outra página como "sem_permissao"

    def get(self, request, doc):
        document = get_object_or_404(Document, id=doc)
        courses = Course.objects.all()
        return render(request, self.template_name, {'document': document, 'courses': courses})

    def post(self, request, doc):
        document = get_object_or_404(Document, id=doc)

        document.title = request.POST.get('title')
        document.author = request.POST.get('author')
        document.year = request.POST.get('year')
        document.type = request.POST.get('type')
        link = request.FILES.get('link')
        if link:
            document.link = link
        document.course_id = request.POST.get('course')
        document.save()

        return redirect('documents')
    
class DocumentDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'confirm-delete.html'
    
    def test_func(self):
        # Só permite se o usuário estiver no grupo "Bibliotecario"
        return self.request.user.groups.filter(name='Bibliotecario').exists()

    def handle_no_permission(self):
        from django.shortcuts import redirect
        # Redireciona se o usuário não tiver permissão (por grupo, por exemplo)
        return redirect('documents.custom')  # ou outra página como "sem_permissao"

    def get(self, request, doc):
        document = get_object_or_404(Document, id=doc)
        return render(request, self.template_name, {'document': document})

    def post(self, request, doc):
        document = get_object_or_404(Document, id=doc)
        document.delete()
        return redirect('documents')

##Logica do Painel do Aluno e Docente

class ListDocumentsCustomView(LoginRequiredMixin, View):
    template_name = 'custom/list-documents.html'
    
    def get(self, request):
        user_groups = request.user.groups.all()
        doc_type = request.GET.get('type')  # ex: 'livro', 'artigo', etc.
        order_by = request.GET.get('order')
        
        # Base query: documentos permitidos ao usuário
        documents = Document.objects.filter(
            group_document_permissions__group__in=user_groups
        )

        # Filtro adicional por tipo, se houver
        if doc_type:
            documents = documents.filter(type__iexact=doc_type)
            
        allowed_orders = ['title', 'type', 'author', 'year']

        if order_by in allowed_orders:
            documents = documents.order_by(order_by)

        documents = documents.distinct()

        return render(request, self.template_name, {
            'documents': documents
        })



class SubmitPrintOrderView(LoginRequiredMixin, View):
    template_name = 'custom/create-order.html'
    
    def get(self, request, id):
        document = get_object_or_404(Document, id=id)
        return render(request, self.template_name, {'document': document})
    
    def post(self, request, id):
        document = get_object_or_404(Document, id=id)
        try:
            copy_total = int(request.POST.get('copy_total', 0))
            firstpage = int(request.POST.get('firstpage', 1))
            lastpage = int(request.POST.get('lastpage', 1))

            if copy_total <= 0 or firstpage <= 0 or lastpage <= 0:
                messages.error(request, "Todos os valores devem ser maiores que zero.")
                return redirect('submit_print_order', id=id)

            if firstpage > lastpage:
                messages.error(request, "A primeira página não pode ser maior que a última.")
                return redirect('submit_print_order', id=id)

            Order.objects.create(
                copy_total=copy_total,
                first_page=firstpage,
                last_page=lastpage,
                status='pendente',
                document=document,
                user=request.user
            )

            messages.success(request, "Pedido de impressão criado com sucesso.")
            return redirect('documents.custom')  # Altere para onde quiser redirecionar após o sucesso

        except ValueError:
            messages.error(request, "Insira apenas números válidos.")
            return redirect('submit_print_order', id=id)

    
class ReadDocumentView(LoginRequiredMixin, View):
    template_name = 'custom/read-document.html'
    
    def get(self, request, id):
        document = get_object_or_404(Document, id=id)
        AcessDocStatistic.objects.create(
            user_id = request.user.id,
            document_id = document.id
        )
        return render(request, self.template_name, {'document':document})