from django.contrib import admin
from .models import Film, Salle, Siege, Seance, Reservation


# ==========================
# FILM
# ==========================
@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('titre', 'genre', 'duree', 'date_sortie')
    list_filter = ('genre',)
    search_fields = ('titre',)


# ==========================
# SALLE
# ==========================
@admin.register(Salle)
class SalleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'nb_lignes', 'nb_colonnes')


# ==========================
# SIÈGE
# ==========================
@admin.register(Siege)
class SiegeAdmin(admin.ModelAdmin):
    list_display = ('salle', 'ligne', 'colonne')
    list_filter = ('salle',)


# ==========================
# SÉANCE
# ==========================
@admin.register(Seance)
class SeanceAdmin(admin.ModelAdmin):
    list_display = ('film', 'date', 'heure', 'salle')
    list_filter = ('date', 'film', 'salle')


# ==========================
# RÉSERVATION
# ==========================
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'film_name', 'siege_label', 'date_reservation')

    def film_name(self, obj):
        return obj.seance.film.titre
    film_name.short_description = 'Film'

    def siege_label(self, obj):
        return str(obj.siege)
    siege_label.short_description = 'Siège'

    list_filter = ('seance__film',)
    search_fields = ('user__username',)