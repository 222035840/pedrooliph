# contatos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Contato
from .forms import ContatoForm

@login_required
def contato_list(request):
    contatos = Contato.objects.all()
    return render(request, "contatos/contato_list.html", {"contatos": contatos})

@login_required
def contato_create(request):
    if request.method == "POST":
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contato_list")
    else:
        form = ContatoForm()
    return render(request, "contatos/contato_form.html", {"form": form})

@login_required
def contato_update(request, pk):
    contato = get_object_or_404(Contato, pk=pk)
    if request.method == "POST":
        form = ContatoForm(request.POST, instance=contato)
        if form.is_valid():
            form.save()
            return redirect("contato_list")
    else:
        form = ContatoForm(instance=contato)
    return render(request, "contatos/contato_form.html", {"form": form})

@login_required
def contato_delete(request, pk):
    contato = get_object_or_404(Contato, pk=pk)
    if request.method == "POST":
        contato.delete()
        return redirect("contato_list")
    return render(request, "contatos/contato_confirm_delete.html", {"contato": contato})
