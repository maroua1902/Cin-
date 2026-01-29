from django.db import models
from django.contrib.auth.models import User


class Film(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('Drame', 'Drame'),
        ('Comédie', 'Comédie'),
        ('Horreur', 'Horreur'),
        ('Romance', 'Romance'),
        ('Comédie musicale', 'Comédie musicale'),
        ('Guerre', 'Guerre'),
        ('Science-Fiction', 'Science-Fiction'),
        ('Autre', 'Autre'),
    ]

    titre = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='Autre')
    duree = models.PositiveIntegerField(help_text="Durée en minutes")
    date_sortie = models.DateField(null=True, blank=True)
    affiche = models.ImageField(upload_to="affiches/", blank=True, null=True)

    def duree_h_min(self):
        h = self.duree // 60
        m = self.duree % 60
        return f"{h}h {m}min"

    def __str__(self):
        return self.titre

class Salle(models.Model):
    nom = models.CharField(max_length=10)
    nb_lignes = models.PositiveIntegerField(default=5)
    nb_colonnes = models.PositiveIntegerField(default=8)

    def __str__(self):
        return self.nom


class Seance(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="seances")
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    date = models.DateField()
    heure = models.TimeField()

    def __str__(self):
        return f"{self.film.titre} — {self.date} à {self.heure}"


class Siege(models.Model):
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    ligne = models.PositiveIntegerField()
    colonne = models.PositiveIntegerField()

    class Meta:
        unique_together = ('salle', 'ligne', 'colonne')

    def __str__(self):
        return f"L{self.ligne}C{self.colonne}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE)
    sieges = models.ManyToManyField(Siege)
    date_reservation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.seance} — {self.sieges.count()} sièges"
