from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Adresse
from django.core.exceptions import ValidationError

def validate_address_data(strasse, hausnummer, plz, ort):
    if not strasse:
        raise ValidationError('Die Straße darf nicht leer sein.')
    if not hausnummer:
        raise ValidationError('Die Hausnummer darf nicht leer sein.')
    if not plz or not str(plz).isdigit() or len(str(plz)) != 4:
        raise ValidationError('Die PLZ muss eine vierstellige Zahl sein.')
    if not ort:
        raise ValidationError('Der Ort darf nicht leer sein.')

def index(request):
    return redirect('adressformular')  # Leitet zur Adresseingabe um

def adressformular(request):
    return render(request, 'adressformular.html')

def adresse_speichern(request):
    if request.method == 'POST':
        strasse = request.POST.get('strasse')
        hausnummer = request.POST.get('hausnummer')
        plz = request.POST.get('plz')
        ort = request.POST.get('ort')

        try:
            validate_address_data(strasse, hausnummer, plz, ort)
            neue_adresse = Adresse(
                strasse=strasse,
                hausnummer=hausnummer,
                plz=plz,
                ort=ort,
            )
            neue_adresse.save()
            messages.success(request, 'Adresse erfolgreich gespeichert.')
            return redirect('adressen_anzeigen')
        except ValidationError as e:
            messages.error(request, f'Fehler beim Speichern der Adresse: {", ".join(e.messages)}')
            return render(request, 'adressformular.html', {'request': request})

    return render(request, 'adressformular.html')

def adressen_anzeigen(request):
    adressen = Adresse.objects.all()
    return render(request, 'adressuebersicht.html', {'adressen': adressen})
