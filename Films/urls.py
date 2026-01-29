from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.home, name='home'),


    path('Films/<int:film_id>/', views.film_detail, name='film_detail'),
    path('reservation/<int:seance_id>/', views.reservation, name='reservation'),
    # ici on utilise str: pour passer "1,2,3"
    path('reservation/confirmation/<str:reservation_ids>/', views.reservation_confirmation, name='reservation_confirmation'),
    path('annuler_reservation/<int:reservation_id>/', views.annuler_reservation, name='annuler_reservation'),
    path('mes_reservations/', views.mes_reservations, name='mes_reservations'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
