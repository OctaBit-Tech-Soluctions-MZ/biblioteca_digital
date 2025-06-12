from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from biblioteca.models import Document, Order


class ListOrders(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "admin/list-orders.html"
    
    def test_func(self):
        # Só permite se o usuário estiver no grupo "Bibliotecario"
        return self.request.user.groups.filter(name='Bibliotecario').exists()

    def handle_no_permission(self):
        from django.shortcuts import redirect
        # Redireciona se o usuário não tiver permissão (por grupo, por exemplo)
        return redirect('documents.custom')  # ou outra página como "sem_permissao"
    
    def get(self, request):
        orders = Order.objects.select_related('user', 'document').all()
        return render(request, self.template_name, {'orders': orders})

class ApproveOrder(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/confirm-approve-order.html'
    
    def test_func(self):
        # Só permite se o usuário estiver no grupo "Bibliotecario"
        return self.request.user.groups.filter(name='Bibliotecario').exists()

    def handle_no_permission(self):
        from django.shortcuts import redirect
        # Redireciona se o usuário não tiver permissão (por grupo, por exemplo)
        return redirect('documents.custom')  # ou outra página como "sem_permissao"
    def get(self, request, id):
        order = get_object_or_404(Order, id=id)
        return render(request, self.template_name,{'order':order})
    
    def post(self,request, id):
        order = get_object_or_404(Order, id=id)
        order.status = 'aprovado'
        order.save()
        messages.success(request, "Pedido aprovado com sucesso.")
        return redirect('orders')
    
class RejectOrder(LoginRequiredMixin, UserPassesTestMixin,TemplateView):
    template_name = 'admin/confirm-order.html'
    
    def test_func(self):
        # Só permite se o usuário estiver no grupo "Bibliotecario"
        return self.request.user.groups.filter(name='Bibliotecario').exists()

    def handle_no_permission(self):
        from django.shortcuts import redirect
        # Redireciona se o usuário não tiver permissão (por grupo, por exemplo)
        return redirect('documents.custom')  # ou outra página como "sem_permissao"
    def get(self, request, id):
        order = get_object_or_404(Order, id=id)
        return render(request, self.template_name,{'order':order})
    
    def post(self,request, id):
        order = get_object_or_404(Order, id=id)
        order.status = 'aprovado'
        order.save()
        messages.success(request, "Pedido aprovado com sucesso.")
        return redirect('orders')


##Logica do Painel do Aluno e Docente

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

class ListOrdersHistory(LoginRequiredMixin, View):
    template_name = "custom/order-history.html"

    def get(self, request):
        orders = Order.objects.select_related('user', 'document').filter(user=request.user)
        return render(request, self.template_name, {'orders': orders})