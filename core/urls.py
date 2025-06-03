from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('inicio/', views.home, name='home'),
    path('perfil/', views.profile, name='profile'),
    path('documento/<int:id>/visualizar', views.showDoc, name='view_doc'),
    path('documento/<int:id>/imprimir', views.printDoc, name='print_doc'),
    path('documento/<int:id>/download', views.downloadDoc, name="download_doc"),
]