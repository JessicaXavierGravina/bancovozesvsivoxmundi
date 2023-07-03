from django.shortcuts import render, redirect, reverse
from .models import Dubladore, Usuario, filtrar_dubladores
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FormHomepage, Checkboxform
from django.views import View
from .filters import Filter
from django.db.models import Q
from django.http import JsonResponse
from django.http import JsonResponse
import sqlite3
import json


class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # usuario esta autenticado:
            # redireciona para a homevozes
            return redirect('vox:homevozes')
        else:
            return super().get(request, *args, **kwargs)  # redireciona para a homepage

    def get_success_url(self):
        email = self.request.POST.get("email")
        usuarios = Usuario.objects.filter(email=email)
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
                    #'nome_artistico': row[0],
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


# def filtros(request):
#     if request.method == 'GET':
#         categoria = request.GET.getlist('categoria')
#         genero = request.GET.getlist('genero')
#         canta = request.GET.getlist('canta')
#         orientacao = request. GET.getlist('orientacao')
#         idiomas = request.GET.getlist('idiomas')
#         etnia = request.GET.getlist('etnia')
#         nome_artistico = request.GET.get('nome_artistico')
#
#     kwargs = {}
#     if categoria:
#         kwargs['categoria__in'] = categoria
#     if genero:
#         kwargs['genero__in'] = genero
#     if canta:
#         kwargs['canta__in'] = canta
#     if orientacao:
#         kwargs['orientacao__in'] = orientacao
#     if idiomas:
#         kwargs['idiomas__in'] = idiomas
#     if etnia:
#         kwargs['etnia__in'] = etnia
#
#     queryset = filtrar_dubladores(categoria, **kwargs)
#
#     context = {
#         'results': queryset
#     }
#
#     return render(request, 'homevozes.html', context)

def filtros(request):
    if request.method == 'POST': # If the form has been submitted...
        form = Dubladore(request.POST) # Um form com os dados de POST
        if form.is_valid(): # All validation rules pass
            categoria = form.cleaned_data['categoria']
            etnia = form.cleaned_data['etnia']
            genero = form.cleaned_data['genero']
            orientacao = form.cleaned_data['orientacao']

        else:
            form = Dublare() # Um formulário vazio

    return render_to_response('homevozes.html', {
        'form': form,
        'categoria': categoria,
        'etnia': etnia,
        'genero': genero,
        'orientacao': orientacao
    })




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


class Editarperfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('vox:homevozes')













# class Buscar(ListView):
#     template_name = 'homevozes.html'
#     model = Dubladore
#
#     def get(self, request, *args, **kwargs):
#         filtro = Filter(request.GET, queryset=self.model.objects.all())
#        # resultados = request.POST.getlist('categoria')
#         resultados = filtro.qs
#
#         context = {
#             'filtro': filtro,
#             'resultados': resultados
#         }
#
#         return render(request, self.template_name, context)
#
#    # self.request.get('sports_played', allow_multiple=True)







#         if form.is_valid():
#             genero = form.cleaned_data['genero']
#             etnia = form.cleaned_data['etnia']
#             orientacao_sexual = form.cleaned_data['orientacao_sexual']
#             categoria_voz = form.cleaned_data['categoria_voz']
#
#             if genero:
#                 dubladores = dubladores.filter(genero=genero)
#             if etnia:
#                 dubladores = dubladores.filter(etnia=etnia)
#             if orientacao_sexual:
#                 dubladores = dubladores.filter(orientacao_sexual=orientacao_sexual)
#             if categoria_voz:
#                 dubladores = dubladores.filter(categoria_voz=categoria_voz)
#
#         context = {'form': form, 'dubladores': dubladores}
#         return render(request, 'busca.html', context)

# class Buscar(View):
#     def get(self, request):
#         genero = request.GET.get('genero')
#         etnia = request.GET.get('etnia')
#         orientacao = request.GET.get('orientacao')
#         canta = request.GET.get('canta')
#         pcd = request.GET.get('pcd')
#         nome_artistico = request.GET.get('nome_artistico')
#
#         filters = Q(Filter)
#         if genero:
#             filters |= Q(genero__icontains=genero)
#         if etnia:
#             filters |= Q(etnia__icontains=etnia)
#         if orientacao:
#             filters |= Q(orientacao__icontains=orientacao)
#         if canta:
#             filters |= Q(canta__icontains=canta)
#         if pcd:
#             filters |= Q(pcd__icontains=pcd)
#         if nome_artistico:
#             filters |= Q(nome_artistico__icontains=nome_artistico)
#
#         listings = Dubladore.objects.filter(filters)
#
#         return render(request, 'homevozes.html', {'listings': listings, 'filters': filters})






# def buscar(request):
#     if request.method == 'POST':
#         categorias = request.POST.getlist('categoria')
#         generos = request.POST.getlist('genero')
#         cantas = request.POST.getlist('canta')
#         orientacoes = request.POST.getlist('orientacao')
#         idiomas = request.POST.getlist('idiomas')
#         etnias = request.POST.getlist('etnia')
#         pcds = request.POST.getlist('pcd')
#
#         conn = sqlite3.connect('bv_voxmundi\db.sqlite3')
#         cursor = conn.cursor()
#
#         query = "SELECT * FROM Dubladore WHERE "
#         conditions = []
#
#         for categoria in categorias:
#             conditions.append(f"categoria = '{categoria}'")
#
#         for genero in generos:
#             conditions.append(f"genero = '{genero}'")
#
#         for canta in cantas:
#             conditions.append(f"canta = '{canta}'")
#
#         for orientacao in orientacoes:
#             conditions.append(f"orientacao = '{orientacao}'")
#
#         for idioma in idiomas:
#             conditions.append(f"idiomas = '{idiomas}'")
#
#         for etnia in etnias:
#             conditions.append(f"etnia = '{etnia}'")
#
#         for pcd in pcds:
#             conditions.append(f"pcd = '{pcd}'")
#
#         if conditions:
#             query += " AND ".join(conditions)
#
#         cursor.execute(query)
#         results = cursor.fetchall()
#
#         dubladores = []
#         for row in results:
#             dublador = {
#   #              'nome_artistico': row[0],
#                 'categoria': row[0],
#                 'genero': row[1],
#                 'canta': row[2],
#                 'orientacao': row[3],
#                 'idiomas': row[4],
#                 'etnia': row[5],
#                 'pcd': row[6]
#             }
#             dubladores.append(dublador)
#
#         conn.close()
#
#         return JsonResponse(json.dumps(dubladores), safe=False)


# def form_checkbox(request):
#     if request.method == 'POST':
#         form = CheckBoxForm(request.POST or None)
#
#         if form.is_valid():
#             print(form.cleaned_data)
#     else:
#         form = CheckBoxForm()
#
#     context = {'form': form}
#     return render(request, 'buscar.html', context)


# conn = sqlite3.connect('db.sqlite3')
# cursor = conn.cursor()
#
# # Função para processar o formulário
# def processar_formulario(dados):
#     # Extrair os dados do formulário
#     categoria = request.POST.getlist('categoria')
#     genero = request.POST.getlist('genero')
#     canta = request.POST.getlist('canta')
#     orientacao = request.POST.getlist('orientacao')
#     idiomas = request.POST.getlist('idiomas')
#     etnia = request.POST.getlist('etnia')
#     pcd = request.POST.getlist('pcd')
#
#     # Construir a consulta SQL
#     # Exemplo: SELECT * FROM tabela WHERE categoria IN (?, ?) AND genero IN (?, ?)
#     consulta = "SELECT * FROM Dubladore WHERE categoria IN ({categoria}) AND genero IN ({genero}) AND canta IN ({" \
#                "canta}) AND orientacao IN ({orientacao}) AND idiomas IN ({idiomas}) AND etnia IN ({etnia}) AND pcd IN ({pcd})".format(
#         ', '.join(['?'] * len(categoria)),
#         ', '.join(['?'] * len(genero)),
#         ', '.join(['?'] * len(canta)),
#         ', '.join(['?'] * len(orientacao)),
#         ', '.join(['?'] * len(idiomas)),
#         ', '.join(['?'] * len(etnia)),
#         ', '.join(['?'] * len(pcd))
#     )
#
#     # Executar a consulta
#     cursor.execute(consulta, categoria + genero + canta + orientacao + idiomas + etnia + pcd)
#
#     # Obter os resultados da consulta
#     resultados = cursor.fetchall()
#
#     # Retornar os resultados para exibição no navegador
#     return resultados
#
# # Rotas
# def buscar():
#     resultados = processar_formulario(request.form)
#     return jsonify(resultados)
#
# # Fechar a conexão com o banco de dados após o uso
# conn.close()


# class SearchResultsView(View):
#     def get(self, request):
#         genero = request.GET.get('genero')
#         etnia = request.GET.get('etnia')
#         orientacao = request.GET.get('orientacao')
#         canta = request.GET.get('canta')
#         pcd = request.GET.get('pcd')
#         nome_artistico = request.GET.get('nome_artistico')
#
#         filters = {}
#         if genero:
#             filters['genero__icontains'] = genero
#         if etnia:
#             filters['etnia__icontains'] = etnia
#         if orientacao:
#             filters['orientacao__icontains'] = orientacao
#         if canta:
#             filters['canta__icontains'] = canta
#         if pcd:
#             filters['pcd__icontains'] = pcd
#         if nome_artistico:
#             filters['nome_artistico__icontains'] = nome_artistico
#
#         listings = Dubladore.objects.filter(**filters)
#
#         return render(request, 'buscar.html', {'listings': listings, 'filters': filters})


# class SearchResultsView(View):
#     def get(self, request):
#         genero = request.GET.get('genero')
#         etnia = request.GET.get('etnia')
#         orientacao = request.GET.get('orientacao')
#         canta = request.GET.get('canta')
#         pcd = request.GET.get('pcd')
#         nome_artistico = request.GET.get('nome_artistico')
#
#         listings = Dubladore.objects.all()
#
#         if genero:
#             listings = listings.filter(genero__icontains=genero)
#         if etnia:
#             listings = listings.filter(etnia__icontains=etnia)
#         if orientacao:
#             listings = listings.filter(orientacao__icontains=orientacao)
#         if canta:
#             listings = listings.filter(canta__icontains=canta)
#         if pcd:
#             listings = listings.filter(pcd__icontains=pcd)
#         if nome_artistico:
#             listings = listings.filter(nome_artistico__icontains=nome_artistico)
#
#         return render(request, 'buscar.html', {'listings': listings})


# class SearchResultsView(View):
#     def get(self, request):
#         genero = request.GET.get('genero')
#         etnia = request.GET.get('etnia')
#         orientacao = request.GET.get('orientacao')
#         canta = request.GET.get('canta')
#         pcd = request.GET.get('pcd')
#
#         listings = Dubladore.objects.all()
#
#         if genero:
#             listings = listings.filter(genero=genero)
#         if etnia:
#             listings = listings.filter(etnia=etnia)
#         if orientacao:
#             listings = listings.filter(orientacao=orientacao)
#         if canta:
#             listings = listings.filter(canta=canta)
#         if pcd:
#             listings = listings.filter(pcd=pcd)
#
#         return render(request, 'buscar.html', {'listings': listings})


# class DubladoreSearchForm(forms.Form):
#     categoria = forms.ChoiceField(choices=LISTA_VOZ_CATEGORIAS, required=False)
#     etnia = forms.ChoiceField(choices=LISTA_ETNIA, required=False)
#     genero = forms.ChoiceField(choices=LISTA_ID_GENERO, required=False)
#     orientacao = forms.ChoiceField(choices=LISTA_ORIENTACAOSEXUAL, required=False)
#
#     def search(self):
#         categoria = self.cleaned_data.get('categoria')
#         etnia = self.cleaned_data.get('etnia')
#         genero = self.cleaned_data.get('genero')
#         orientacao = self.cleaned_data.get('orientacao')
#
#         results = Dubladore.objects.all()
#
#         if categoria:
#             results = results.filter(categoria=categoria)
#
#         if etnia:
#             results = results.filter(etnia=etnia)
#
#         if genero:
#             results = results.filter(genero=genero)
#
#         if orientacao:
#             results = results.filter(orientacao=orientacao)
#
#         return results


# class DubladoreSearchView:
#     template_name = 'buscar.html'
#     form_class = DubladoreSearchForm
#
#     def get(self, request):
#         form = self.form_class(request.GET or None)
#         results = None
#
#         if form.is_valid():
#             results = form.search()
#
#         return render(request, self.template_name, {'form': form, 'results': results})
