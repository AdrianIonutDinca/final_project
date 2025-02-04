from django.db import models
from django.db.models import *
from django.contrib.auth.models import User
from django.utils.timezone import now


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
    judet = CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f'{self.magazin} ({self.judet})'






class OperatorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    judet = models.CharField(max_length=128, blank=True, null=True)  # Câmp pentru județ

    def __str__(self):
        return f"{self.user.username} - {self.judet or 'Fără județ'}"


class Cerere(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cereri')
    data_cerere = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cerere de la {self.client.username} din {self.data_cerere}"


class Preturi(models.Model):
    cerere = models.ForeignKey(Cerere, on_delete=models.CASCADE, related_name='preturi')
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE)
    magazin = models.ForeignKey(Magazin, on_delete=models.CASCADE)
    pret = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produs.denumire} - {self.magazin.magazin}: {self.pret} lei"

class SelectedData(models.Model):
    product = models.ForeignKey(Produs, on_delete=models.CASCADE)
    store = models.ForeignKey(Magazin, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Prețul, inițial NULL
    created_at = models.DateTimeField(default=now, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Selected Data'

    def __str__(self):
        return f'{self.product.denumire} - {self.store.magazin}'

class SavedPrices(models.Model):
    product = models.ForeignKey(Produs, on_delete=models.CASCADE)
    store = models.ForeignKey(Magazin, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    operator = models.ForeignKey(User, on_delete=models.CASCADE)  # Utilizatorul care a salvat datele
    date_saved = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Saved Prices'

    def __str__(self):
        return f'{self.product.denumire} - {self.store.magazin} - {self.price}'