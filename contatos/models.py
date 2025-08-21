# contatos/models.py
from django.db import models

class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nome
