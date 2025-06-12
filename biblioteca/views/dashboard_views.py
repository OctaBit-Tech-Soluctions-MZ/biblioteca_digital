import locale
from django.views import View
from ..dashboard_service import (
    get_recent_users,
    get_documents_this_month,
    get_order_status_counts,
    calculate_order_completion_percentage,
    get_access_stats_by_month,
    get_recent_access,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.utils import timezone
from biblioteca.models import Document, User, Order, AcessDocStatistic

class DashboardAdminView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'admin/dashboard.html'
    
    def test_func(self):
        # Só permite se o usuário estiver no grupo "Bibliotecario"
        return self.request.user.groups.filter(name='Bibliotecario').exists()

    def handle_no_permission(self):
        from django.shortcuts import redirect
        # Redireciona se o usuário não tiver permissão (por grupo, por exemplo)
        return redirect('login')  # ou outra página como "sem_permissao"

    def get(self, request):
        total_users = User.objects.count()
        total_documents = Document.objects.count()
        total_orders = Order.objects.count()
        total_access = AcessDocStatistic.objects.count()
        recent_users = get_recent_users()
        documents_this_month = get_documents_this_month()
        order_status_counts = get_order_status_counts()
        status_counts = {item['status']: item['count'] for item in order_status_counts}
        total_orders_complete = calculate_order_completion_percentage(status_counts, total_orders)
        access_stats_by_month = get_access_stats_by_month()
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8') 
        total_access_recent = get_recent_access()

        context = {
            'recent_users': recent_users,
            'documents_this_month': documents_this_month,
            'current_month_year': timezone.now().strftime('%B'),
            'total_users': total_users,
            'total_documents': total_documents,
            'total_orders': total_orders,
            'total_orders_complete': total_orders_complete,
            'access_stats_by_month': access_stats_by_month,
            'total_access' : total_access,
            'total_access_recent': total_access_recent
        }
        return render(request, self.template_name, context)
