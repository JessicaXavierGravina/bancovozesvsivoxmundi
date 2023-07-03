import django_filters
from .models import Dubladore

class Filter(django_filters.FilterSet):

    categoria = django_filters.ModelMultipleChoiceFilter(queryset=Dubladore.objects.all(), to_field_name='categoria')
    etnia = django_filters.ModelMultipleChoiceFilter(queryset=Dubladore.objects.all(), to_field_name='etnia')
    genero = django_filters.ModelMultipleChoiceFilter(queryset=Dubladore.objects.all(), to_field_name='genero')
    orientacao = django_filters.ModelMultipleChoiceFilter(queryset=Dubladore.objects.all(), to_field_name='orientacao')
    idiomas = django_filters.ModelMultipleChoiceFilter(queryset=Dubladore.objects.all(), to_field_name='idiomas')
    pcd = django_filters.ModelMultipleChoiceFilter(queryset=Dubladore.objects.all(), to_field_name='pcd')
    canta = django_filters.ModelMultipleChoiceFilter(queryset=Dubladore.objects.all(), to_field_name='canta')
    extensao_vocal = django_filters.ModelMultipleChoiceFilter(queryset=Dubladore.objects.all(), to_field_name='extensao_vocal')
    nascimento = django_filters.ModelMultipleChoiceFilter(queryset=Dubladore.objects.all(), to_field_name='nascimento')


    class Meta:
        model = Dubladore
        fields = ['categoria', 'etnia', 'genero', 'orientacao', 'idiomas', 'pcd', 'canta', 'extensao_vocal', 'nascimento' ]  # Lista dos campos que deseja filtrar
