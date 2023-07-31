import json
import sqlite3


from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView, UpdateView

from .forms import FormHomepage
from .models import Dubladore, Usuario


class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # usuario esta autenticado:
            # redireciona para a homevozes
            return redirect('vox:homevozes')
        else:
            return super().get(request, *args, **kwargs)  # redireciona para a homepage

    from django.views.decorators.csrf import csrf_exempt
    @csrf_exempt
    def get_success_url(self):
        email = self.request.POST.get("email")
        password = self.request.POST['password']
        usuarios = Usuario.objects.filter(email=email, password=password)
        if usuarios:
            return reverse('vox:login')
        else:
            return reverse('vox:homepage')


class Homevozes(LoginRequiredMixin, ListView):
    template_name = "homevozes.html"
    model = Dubladore

    def buscar(request):
        if request.method == 'GET':
            categoria = request.GET.getlist('categoria')
            genero = request.GET.getlist('genero')
            canta = request.GET.getlist('canta')
            orientacao = request.GET.getlist('orientacao')
            idioma = request.GET.getlist('idiomas')
            etnia = request.GET.getlist('etnia')
            pcd = request.GET.getlist('pcd')

            conn = sqlite3.connect('bv_voxmundi\db.sqlite3')
            cursor = conn.cursor()

            query = "SELECT * FROM Dubladore WHERE "
            conditions = []

            for categoria in categoria:
                conditions.append(f"categoria = '{categoria}'")

            for genero in genero:
                conditions.append(f"genero = '{genero}'")

            for canta in canta:
                conditions.append(f"canta = '{canta}'")

            for orientacao in orientacao:
                conditions.append(f"orientacao = '{orientacao}'")

            for idioma in idioma:
                conditions.append(f"idioma = '{idioma}'")

            for etnia in etnia:
                conditions.append(f"etnia = '{etnia}'")

            for pcd in pcd:
                conditions.append(f"pcd = '{pcd}'")

            if conditions:
                query += " AND ".join(conditions)

            cursor.execute(query)
            results = cursor.fetchall()

            dubladores = []
            for row in results:
                dublador = {
                    # 'nome_artistico': row[0],
                    'categoria': row[0],
                    'genero': row[1],
                    'canta': row[2],
                    'orientacoes': row[3],
                    'idioma': row[4],
                    'etnias': row[5],
                    'pcds': row[6]
                }
                dubladores.append(dublador)

            conn.close()

            return JsonResponse(json.dumps(dubladores), safe=False)


class Detalhesvoz(LoginRequiredMixin, DetailView):
    template_name = "detalhesvoz.html"
    model = Dubladore

    def get(self, request, *args, **kwargs):
        dublador = self.get_object()
        dublador.save()
        usuario = request.user
        usuario.dubladores_vistos.add(dublador)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dublador_atual = self.get_object()
        vozes_relacionadas = Dubladore.objects.filter(categoria=dublador_atual.categoria).exclude(pk=dublador_atual.pk)
        context['vozes_relacionadas'] = vozes_relacionadas
        return context


class Pesquisa(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Dubladore

    # object_list
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = Dubladore.objects.filter(nome_artistico__icontains=termo_pesquisa)
            return object_list
        else:
            return None


# ESSE FILTRO
class Filtro(LoginRequiredMixin, ListView):
    template_name = "buscar.html"
    model = Dubladore

    # object_list
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = Dubladore.objects.filter(categoria__icontains=termo_pesquisa)
            return object_list
        else:
            return None


class Editarperfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('vox:homevozes')


class Editardublador(LoginRequiredMixin, DetailView):
    template_name = "detalhesvoz.html"
    model = Dubladore

    def get(self, request, *args, **kwargs):
        dublador = self.get_object()
        usuario = request.user
        usuario.dubladores_vistos.add(dublador)
        return redirect('admin:vox_dubladore_change', object_id=dublador.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dublador_atual = self.get_object()
        vozes_relacionadas = Dubladore.objects.filter(categoria=dublador_atual.categoria)
        context['vozes_relacionadas'] = vozes_relacionadas
        return context


class Editardublador(LoginRequiredMixin, DetailView):
    template_name = "detalhesvoz.html"
    model = Dubladore

    def get(self, request, *args, **kwargs):
        dublador = self.get_object()
        usuario = request.user
        usuario.dubladores_vistos.add(dublador)
        return redirect('admin:vox_dubladore_change', object_id=dublador.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dublador_atual = self.get_object()
        vozes_relacionadas = Dubladore.objects.filter(categoria=dublador_atual.categoria)
        context['vozes_relacionadas'] = vozes_relacionadas
        return context


class AdicionarDubladorView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return redirect('/admin/vox/dubladore/add/')
