from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Film, Reservation, Siege, Seance


def index(request):
    return render(request, 'Films/index.html')


@login_required(login_url='login')
def home(request):
    genre = request.GET.get('genre')
    films = Film.objects.all()

    if genre:
        films = films.filter(genre=genre)

    reservations = Reservation.objects.filter(user=request.user)

    return render(request, 'Films/home.html', {
        'films': films,
        'reservations': reservations,
        'genre': genre
    })


def film_detail(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    seances = film.seances.all()

    return render(request, 'Films/film_detail.html', {
        'film': film,
        'seances': seances
    })


@login_required(login_url='login')
def reservation(request, seance_id):
    seance = get_object_or_404(Seance, id=seance_id)

    # Tous les sièges de la salle
    sieges = Siege.objects.filter(salle=seance.salle).order_by('ligne', 'colonne')

    # Récupérer les sièges déjà réservés pour cette séance
    reservations_existantes = Reservation.objects.filter(seance=seance)
    sieges_reserves_ids = reservations_existantes.values_list('sieges__id', flat=True)

    # Attribut temporaire pour le template
    for siege in sieges:
        siege.reserve = siege.id in sieges_reserves_ids

    error = None

    if request.method == "POST":
        siege_ids = request.POST.getlist("sieges")  # multiple sélection
        if not siege_ids:
            error = "Vous devez sélectionner au moins un siège."
        else:
            # Vérifier qu’aucun siège n’est déjà réservé
            for sid in siege_ids:
                if int(sid) in sieges_reserves_ids:
                    error = "Un des sièges sélectionnés est déjà réservé."
                    break

            if not error:
                reservation_obj = Reservation.objects.create(user=request.user, seance=seance)
                reservation_obj.sieges.add(*siege_ids)
                return redirect('reservation_confirmation', reservation_ids=",".join(siege_ids))

    return render(request, 'Films/reservation.html', {
        'seance': seance,
        'sieges': sieges,
        'error': error
    })


@login_required
def reservation_confirmation(request, reservation_ids):
    siege_ids = reservation_ids.split(',')
    sieges = Siege.objects.filter(id__in=siege_ids)
    return render(request, 'Films/reservation_confirmation.html', {'reservations': sieges})



@login_required
def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    reservation.delete()
    return redirect('home')



def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'Films/login.html', {
                'error': 'Nom ou mot de passe incorrect'
            })

    return render(request, 'Films/login.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'Films/register.html', {
                'error': 'Ce nom d’utilisateur existe déjà'
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'Films/register.html')
@login_required
def mes_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-date_reservation')
    return render(request, 'Films/mes_reservations.html', {'reservations': reservations})
