# contatos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.contato_list, name='contato_list'),
    path('novo/', views.contato_create, name='contato_create'),
    path('<int:pk>/editar/', views.contato_update, name='contato_update'),
    path('<int:pk>/deletar/', views.contato_delete, name='contato_delete'),
]
