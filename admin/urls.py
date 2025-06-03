from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name="dashboard"),
    path('pedidos', views.admin_dashboard, name="orders"),
    path('utilizadores', views.listUser, name="users"),
    path('utilizadores/registar', views.registerUser, name="create-user"),
    path('documentos', views.listDocument, name="documents"),
    path('documentos/registar', views.registerDocument, name="registerdoc"),
]