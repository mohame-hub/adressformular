from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from pip._vendor import requests2
from .models import Adresse
from .views import validate_address_data


class AdresseModelTest(TestCase):
    def test_create_adresse(self):
        # Test for successful creation of an Adresse instance
        adresse = Adresse.objects.create(
            strasse="Teststraße",
            hausnummer="1A",
            plz="1234",
            ort="Teststadt",
            bundesland="Testland"
        )
        self.assertEqual(str(adresse), "Teststraße 1A, 1234 Teststadt, Testland")
        self.assertEqual(Adresse.objects.count(), 1)

class AdresseViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_adressformular_view(self):
        response = self.client.get(reverse('adressformular'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adressformular.html')

    def test_adresse_speichern_valid(self):
        response = self.client.post(reverse('adresse_speichern'), {
            'strasse': 'Hauptstraße',
            'hausnummer': '42',
            'plz': '1234',
            'ort': 'Musterstadt'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after success
        self.assertEqual(Adresse.objects.count(), 1)  # One address saved
        self.assertEqual(Adresse.objects.first().strasse, 'Hauptstraße')



    def test_adressen_anzeigen_view(self):
        Adresse.objects.create(
            strasse="Hauptstraße",
            hausnummer="42",
            plz="1234",
            ort="Musterstadt"
        )
        response = self.client.get(reverse('adressen_anzeigen'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hauptstraße')

class AdresseValidationTest(TestCase):
    def test_validate_address_data(self):
        try:
            validate_address_data("Hauptstraße", "42", "1234", "Musterstadt")
        except ValidationError:
            self.fail("validate_address_data raised ValidationError unexpectedly!")

    def test_validate_address_data_invalid(self):
        with self.assertRaises(ValidationError):
            validate_address_data("", "42", "1234", "Musterstadt")


class ExterneAPITests(TestCase):
    def test_fetch_adress_data(self):
        url = "https://data.wien.gv.at/daten/OGDAddressService.svc/GetAddressInfo?Address=Spengergasse"

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)  # Prüfen, ob der API-Aufruf erfolgreich war

        data = response.json()
        self.assertIn('features', data)
        self.assertGreater(len(data['features']), 0, "Es sollten Adressen gefunden werden.")
