from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser

LISTA_VOZ_CATEGORIAS = {

    ("Infantil Feminina", "Infantil Feminina"),
    ("Infantil Masculina", "Infantil Masculina"),
    ("Adolescente Feminina", "Adolescente Feminina"),
    ("Adolescente Masculina", "Adolescente Masculina"),
    ("Jovem Feminina Leve", "Jovem Feminina Leve"),
    ("Jovem Feminina", "Jovem Feminina"),
    ("Jovem Feminina Pesada", "Jovem Feminina Pesada"),
    ("Jovem Masculina Leve", "Jovem Masculina Leve"),
    ("Jovem Masculina", "Jovem Masculina"),
    ("Jovem Masculina Pesada", "Jovem Masculina Pesada"),
    ("Adulta Feminina Leve", "Adulta Feminina Leve"),
    ("Adulta Feminina", "Adulta Feminina"),
    ("Adulta Feminina Pesada", "Adulta Feminina Pesada"),
    ("Adulta Masculina Leve", "Adulta Masculina Leve"),
    ("Adulta Masculina", "Adulta Masculina"),
    ("Adulta Masculina Pesada", "Adulta Masculina Pesada"),
    ("Meia Idade Feminina", "Meia Idade Feminina"),
    ("Meia Idade Masculina", "Meia Idade Masculina"),
    ("Idosa Feminina Leve", "Idosa Feminina Leve"),
    ("Idosa Feminina", "Idosa Feminina"),
    ("Idosa Feminina Pesada", "Idosa Feminina Pesada"),
    ("Idosa Masculina Leve", "Idosa Masculina Leve"),
    ("Idosa Masculina", "Idosa Masculina"),
    ("Idosa Masculina Pesada", "Idosa Masculina Pesada"),

}

LISTA_ETNIA = (

    ("Amarela", "Amarela"),
    ("Branca", "Branca"),
    ("Indigena", "Indigena"),
    ("Parda", "Parda"),
    ("Preta", "Preta"),
    ("Não Informado", "Não Informado"),

)

LISTA_ORIENTACAOSEXUAL = (

    ("Assexual", "Assexual"),
    ("Bissexual", "Bissexual"),
    ("Heterossexual", "Heterossexual"),
    ("Homossexual", "Homossexual"),
    ("Pansexual", "Pansexual"),
    ("Não Informado", "Não Informado"),

)

LISTA_ID_GENERO = (

    ("Homem Cis", "Homem Cis"),
    ("Homem Trans", "Homem Trans"),
    ("intersexo", "intersexo"),
    ("Mulher Cis", "Mulher Cis"),
    (" Mulher Trans", " Mulher Trans"),
    ("Não Binário", "Não Binário"),
    ("Não Informado", "Não Informado"),

)


class Dubladore(models.Model):

    dublador = models.CharField(max_length=100)
    nome_artistico = models.CharField(max_length=40)
    nascimento = models.DateField(verbose_name=_('Data de Nascimento'))
    categoria = models.CharField(max_length=2500, choices=LISTA_VOZ_CATEGORIAS)
    etnia = models.CharField(max_length=1000, choices=LISTA_ETNIA)
    genero = models.CharField(max_length=1000, choices=LISTA_ID_GENERO)
    orientacao = models.CharField(max_length=1000, choices=LISTA_ORIENTACAOSEXUAL)
    idiomas = models.CharField(max_length=60)
    pcd = models.CharField(default="Não",max_length=3, choices=(('Sim', 'Sim'),('Não', 'Nâo')))
    canta = models.CharField(default="Não", max_length=3, choices=(('Sim', 'Sim'), ('Não', 'Nâo')))
    extensao_vocal = models.TextField(max_length=1000)
    foto = models.ImageField(upload_to='foto_dublador', default='default.png')
    audio = models.FileField(upload_to='music/')
    audio2 = models.FileField(upload_to='music/', blank = True)
    audio3 = models.FileField(upload_to='music/', blank = True)
    audio4 = models.FileField(upload_to='music/', blank = True)
    audio5 = models.FileField(upload_to='music/', blank = True)
    audio6 = models.FileField(upload_to='music/', blank = True)


    def __str__(self):
        return self.nome_artistico


class Usuario(AbstractUser):
    dubladores_vistos = models.ManyToManyField("Dubladore")



def filtrar_dubladores( categorias, **kwargs):
    resultados = Dubladore.objects.all()

    if categorias:
        resultados = resultados.filter(categoria__in=categorias)
    if kwargs:
        resultados = resultados.filter(**kwargs)

    return resultados