# contatos/tests.py
from django.test import TestCase
from .models import Contato

class ContatoModelTest(TestCase):
    def test_criacao_contato(self):
        contato = Contato.objects.create(
            nome="Pedro Pinheiro", email="pedro@email.com", telefone="61999999999"
        )
        self.assertEqual(str(contato), "Pedro Pinheiro")
