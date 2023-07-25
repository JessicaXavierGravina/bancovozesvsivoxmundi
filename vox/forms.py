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

