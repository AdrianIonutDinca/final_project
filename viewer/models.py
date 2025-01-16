from django.db import models
from django.db.models import *

# Create your models here.
class Categ(models.Model):

    # class Meta este o clasa creata in interiorul modelului
    # contine proprietati ale modelului care pot fi schimbate
    class Meta:
        # attributul 'verbose_name_plural' este numele care va aparea pe pagina de admin
        # exemplu:
        verbose_name_plural = 'Categorii de produse'

    # Field in modelul Genre numit 'name' care este de tip CharField (mai exact, un string)
    # max_length este un parametru care indica lungimea maxima al acestui field
    name = CharField(max_length=128)

    def __str__(self):
        return self.name

class Produs(models.Model):

    class Meta:
        verbose_name_plural = 'Produse'

    denumire = CharField(max_length=128)

    # IntegerField este un field care simbolizeaza un simplu int
    garantie_luni = IntegerField()

    # DateField este un field in care o sa se salveze un obiect Date care include zi, luna, an
    lansat = DateField()

    # TextField va contine un simplu string, indiferent de lungimea lui
    descriere = TextField()

    # ForeignKey face referire la un alt tabel din baza de date
    # on_delete insemna ce actiune se va intempla cand randul la care facem referire este sters
    # DO_NOTHING inseamna ca nu se va intampla nimic
    categ = ForeignKey(Categ, on_delete=DO_NOTHING)

    # DateTimeField este un field care va contine zi, luna, an, ora, minut
    # auto_now_add specifica daca sa va completa campul automat cand este salvat obiectul
    created = DateTimeField(auto_now_add=True)

    # ManyToMany insemna ca un film poate avea mai multi actori
    # si un actor poate fi parte din mai multe filme
    # Magazine = ManyToManyField(Magazin)

    def __str__(self):
        return f'{self.denumire}'

class Magazin(models.Model):

    class Meta:
        verbose_name_plural = 'Magazine'

    magazin = CharField(max_length=128)
    retea = CharField(max_length=128)

    def __str__(self):
        return f'{self.magazin}'


