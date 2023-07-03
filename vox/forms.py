from django import forms
from .models import Dubladore

class FormHomepage(forms.Form):
    email = forms.EmailField(label=False)


class Checkboxform(forms.ModelForm):

    class Meta:
        model = Dubladore
        fields = ("nome_artistico", "categoria", "etnia", "genero", "orientacao", "idiomas")


class CheckBoxForm(forms.Form):
    class Meta:
        model = Dubladore

        categoria = forms.BooleanField(required=False)
        genero = forms.BooleanField(required=False)
        canta = forms.BooleanField(required=False)
        orientacao = forms.BooleanField(required=False)
        etnia = forms.BooleanField(required=False)
        pcd = forms.BooleanField(required=False)




# class DubladoreSearchForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['categoria'] = forms.ChoiceField(choices=Dubladore.LISTA_VOZ_CATEGORIAS, required=False)
#         self.fields['etnia'] = forms.ChoiceField(choices=Dubladore.LISTA_ETNIA, required=False)
#         self.fields['genero'] = forms.ChoiceField(choices=Dubladore.LISTA_ID_GENERO, required=False)
#         self.fields['orientacao'] = forms.ChoiceField(choices=Dubladore.LISTA_ORIENTACAOSEXUAL, required=False)
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
#
#
# class DubladoreSearchView:
#     template_name = 'dubladore_search.html'
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

