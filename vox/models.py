from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser

LISTA_VOZ_CATEGORIAS = {

    ("InfantilFeminina", "Infantil Feminina"),
    ("InfantilMasculina", "Infantil Masculina"),
    ("AdolescenteFeminina", "Adolescente Feminina"),
    ("AdolescenteMasculina", "Adolescente Masculina"),
    ("JovemFemininaLeve", "Jovem Feminina Leve"),
    ("JovemFeminina", "Jovem Feminina"),
    ("JovemFemininaPesada", "Jovem Feminina Pesada"),
    ("JovemMasculinaLeve", "Jovem Masculina Leve"),
    ("JovemMasculina", "Jovem Masculina"),
    ("JovemMasculinaPesada", "Jovem Masculina Pesada"),
    ("AdultaFemininaLeve", "Adulta Feminina Leve"),
    ("AdultaFeminina", "Adulta Feminina"),
    ("AdultaFemininaPesada", "Adulta Feminina Pesada"),
    ("AdultaMasculinaLeve", "Adulta Masculina Leve"),
    ("AdultaMasculina", "Adulta Masculina"),
    ("AdultaMasculinaPesada", "Adulta Masculina Pesada"),
    ("MeiaIdadeFeminina", "Meia Idade Feminina"),
    ("MeiaIdadeMasculina", "Meia Idade Masculina"),
    ("IdosaFemininaLeve", "Idosa Feminina Leve"),
    ("IdosaFeminina", "Idosa Feminina"),
    ("IdosaFemininaPesada", "Idosa Feminina Pesada"),
    ("IdosaMasculinaLeve", "Idosa Masculina Leve"),
    ("IdosaMasculina", "Idosa Masculina"),
    ("IdosaMasculinaPesada", "Idosa Masculina Pesada"),

}

LISTA_ETNIA = (

    ("Amarela", "Amarela"),
    ("Branca", "Branca"),
    ("Indigena", "Indigena"),
    ("Parda", "Parda"),
    ("Preta", "Preta"),
    ("NaoInformado", "Não Informado"),

)

LISTA_ORIENTACAOSEXUAL = (

    ("Assexual", "Assexual"),
    ("Bissexual", "Bissexual"),
    ("Heterossexual", "Heterossexual"),
    ("Homossexual", "Homossexual"),
    ("Pansexual", "Pansexual"),
    ("NaoInformado", "Não Informado"),

)

LISTA_ID_GENERO = (

    ("HomemCis", "Homem Cis"),
    ("HomemTrans", "Homem Trans"),
    ("intersexo", "intersexo"),
    ("MulherCis", "Mulher Cis"),
    (" MulherTrans", " Mulher Trans"),
    ("NaoBinario", "Não Binário"),
    ("NaoInformado", "Não Informado"),

)


class Dubladore(models.Model):
    objects = None
    dublador = models.CharField(max_length=100, blank=True)
    nome_artistico = models.CharField(max_length=40, blank=True)
    nascimento = models.DateField(verbose_name=_('Data de Nascimento'), null=True, blank=True)
    categoria = models.CharField(max_length=2500, choices=LISTA_VOZ_CATEGORIAS, blank=True)
    etnia = models.CharField(max_length=1000, choices=LISTA_ETNIA, blank=True)
    genero = models.CharField(max_length=1000, choices=LISTA_ID_GENERO, blank=True)
    orientacao = models.CharField(max_length=1000, choices=LISTA_ORIENTACAOSEXUAL, blank=True)
    idiomas = models.CharField(max_length=60, blank=True)
    pcd = models.CharField(default="Não", max_length=3, choices=(('Sim', 'Sim'), ('Não', 'Nâo')), blank=True)
    canta = models.CharField(default="Não", max_length=3, choices=(('Sim', 'Sim'), ('Não', 'Nâo')), blank=True)
    extensao_vocal = models.TextField(max_length=1000, blank=True)
    foto = models.ImageField(upload_to='foto_dublador', default='default.png', blank=True)
    audio = models.FileField(upload_to='music/')
    audio2 = models.FileField(upload_to='music/', blank=True)
    audio3 = models.FileField(upload_to='music/', blank=True)
    audio4 = models.FileField(upload_to='music/', blank=True)
    audio5 = models.FileField(upload_to='music/', blank=True)
    audio6 = models.FileField(upload_to='music/', blank=True)

    def __str__(self):
        return self.nome_artistico


class Usuario(AbstractUser):
    dubladores_vistos = models.ManyToManyField("Dubladore")


def filtrar_dubladores(categorias, **kwargs):
    resultados = Dubladore.objects.all()

    if categorias:
        resultados = resultados.filter(categoria__in=categorias)
    if kwargs:
        resultados = resultados.filter(**kwargs)

    return resultados
