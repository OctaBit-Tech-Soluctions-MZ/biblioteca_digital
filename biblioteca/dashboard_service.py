from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count
from .models import Document, Order, AcessDocStatistic, User


def get_recent_users(days=7):
    """Retorna a quantidade de usuários registrados nos últimos `days` dias."""
    seven_days_ago = timezone.now() - timezone.timedelta(days=days)
    return User.objects.filter(date_joined__gte=seven_days_ago).count()

def get_recent_access(days=7):
    """Retorna a quantidade de acesso da plataforma nos últimos `days` dias."""
    seven_days_ago = timezone.now() - timezone.timedelta(days=days)
    return AcessDocStatistic.objects.filter(created_at__gte=seven_days_ago).count()


def get_documents_this_month():
    """Retorna a quantidade de documentos registrados no mês atual."""
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1)
    return Document.objects.filter(
        created_at__gte=start_of_month,
        created_at__lt=next_month
    ).count()


def get_order_status_counts():
    """
    Retorna a contagem de pedidos para cada status.
    Exemplo de retorno: [{'status': 'pendente', 'count': 5}, {'status': 'aprovado', 'count': 12}]
    """
    order_status_counts = Order.objects.values('status').annotate(count=Count('status'))
    return order_status_counts


def calculate_order_completion_percentage(status_counts, total_orders):
    """
    Calcula a porcentagem de pedidos 'aprovado' + 'rejeitado' em relação ao total.
    """
    if total_orders == 0:
        return 0
    aprovado = status_counts.get('aprovado', 0)
    rejeitado = status_counts.get('rejeitado', 0)
    return round(((aprovado + rejeitado) * 100) / total_orders, 2)


def get_access_stats_by_month():
    """Retorna estatísticas de acessos de documentos agrupadas por mês."""
    return (
        AcessDocStatistic.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )
