from django.urls import path, include
from adressformular import views

urlpatterns = [
    path('', views.index, name='index'),
    # Route zum Rendern des Adressformulars
    path('adressformular/', views.adressformular, name='adressformular'),

    # API-Endpunkt zum Speichern der eingegebenen Adresse
    path('adresse_speichern/', views.adresse_speichern, name='adresse_speichern'),

    # Route zur Anzeige aller gespeicherten Adressen
    path('adressen_anzeigen/', views.adressen_anzeigen, name='adressen_anzeigen'),
]
