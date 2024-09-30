from django.urls import path
from . import views  # Importiere die Views aus der aktuellen App

urlpatterns = [
    # Route zum Rendern des Adressformulars
    path('adressformular/', views.adressformular, name='adressformular'),

    # API-Endpunkt zum Speichern der eingegebenen Adresse
    path('adresse_speichern/', views.adresse_speichern, name='adresse_speichern'),

    # Route zur Anzeige aller gespeicherten Adressen
    path('adressen_anzeigen/', views.adressen_anzeigen, name='adressen_anzeigen'),
]
