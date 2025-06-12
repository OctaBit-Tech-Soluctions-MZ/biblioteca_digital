from django.urls import path
from .views.document_views import  (
    ListDocuments,
    DocumentUpdateView,
    DocumentCreateView,
    DocumentDeleteView,
    ListDocumentsCustomView,
    ReadDocumentView,
)
from .views.user_views import (
    UserListView,
    CreateUserView,
    CreatedSuccessfullUser
)
from .views.order_views import (
    ListOrders,
    SubmitPrintOrderView,
    ApproveOrder,
    RejectOrder,
    ListOrdersHistory,
)
from .views.courses_views import (
    CoursesView,
    DeleteCourseView
)
from .views.profile_views import ProfileView
from .views.dashboard_views import DashboardAdminView
from .views.login_views import LoginView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('admin/', DashboardAdminView.as_view(), name='admin_dashboard'),
    path('admin/documentos', ListDocuments.as_view(), name='documents'),
    path('admin/documentos/registar', DocumentCreateView.as_view(), name='documents.register'),
    path('admin/documentos/<int:doc>/excluir', DocumentDeleteView.as_view(), name='document.delete'),
    path('admin/documentos/<int:doc>/editar', DocumentUpdateView.as_view(), name='document.edit'),
    path('admin/pedidos', ListOrders.as_view(), name='orders'),
    path('admin/pedidos/<int:id>/aprovar', ApproveOrder.as_view(), name='orders.approve'),
    path('admin/pedidos/<int:id>/rejeitar', RejectOrder.as_view(), name='orders.reject'),
    path('admin/utilizadores', UserListView.as_view(), name='users'),
    path('admin/utilizadores/registar', CreateUserView.as_view(), name='users.register'),
    path('admin/utilizadores/criado-com-sucesso', CreatedSuccessfullUser.as_view(), name='users.successfully'),
    path('admin/cursos', CoursesView.as_view(), name='courses'),
    path('admin/cursos/<int:id>/excluir', DeleteCourseView.as_view(), name='courses.delete'),
    path('perfil', ProfileView.as_view(), name="profile"),
    ###Rotas dos Estudante/Docente
    path('documentos',ListDocumentsCustomView.as_view(), name='documents.custom'),
    path('documentos/<int:id>/submeter-pedido', SubmitPrintOrderView.as_view(), name='order.submit'),
    path('documento/<int:id>/leitura', ReadDocumentView.as_view() , name='documents.read'),
    path('historico-pedidos',ListOrdersHistory.as_view(), name="orders.history"),
]