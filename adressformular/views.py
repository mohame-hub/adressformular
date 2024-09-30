from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Adresse

# View zum Rendern des Adressformulars
def adressformular(request):
    """
    Rendert das Formular zur Eingabe einer Adresse.
    """
    return render(request, 'adresse_formular.html')  # Rendere die Seite mit dem Formular

# API-Endpunkt zum Speichern der eingegebenen Adresse
def adresse_speichern(request):
    if request.method == 'POST':
        # Überprüfen, ob alle Felder ausgefüllt sind
        if not all([request.POST.get('strasse'), request.POST.get('hausnummer'), request.POST.get('plz'),
                    request.POST.get('ort'), request.POST.get('bundesland')]):
            return JsonResponse({'error': 'Bitte alle Felder ausfüllen'}, status=400)

        # Neue Adresse erstellen und speichern
        neue_adresse = Adresse(
            strasse=request.POST['strasse'],
            hausnummer=request.POST['hausnummer'],
            plz=request.POST['plz'],
            ort=request.POST['ort'],
            bundesland=request.POST['bundesland']
        )
        neue_adresse.save()

        # Erfolgreiches Speichern, umleiten zur Adressübersicht
        return redirect('adressen_anzeigen')

    # Wenn es keine POST-Anfrage ist, Fehlermeldung ausgeben
    return JsonResponse({'error': 'Nur POST-Anfragen sind erlaubt'},status=400)
# View zur Anzeige aller gespeicherten Adressen
def adressen_anzeigen(request):
    """
    Zeigt eine Übersicht aller gespeicherten Adressen.
    """
    adressen = Adresse.objects.all()  # Hole alle Adressen aus der Datenbank
    return render(request, 'adressen_anzeigen.html', {'adressen': adressen})  # Rendere die Seite mit der Adressenliste
