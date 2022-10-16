from django.test import TestCase
from django.shortcuts import reverse

# Create your tests here.

class LandingPageTest(TestCase):
    def test_status_code(self):
        response = self.client.get(reverse("landing-page"))
        print(response.status_code)

    def test_template_name(self):
        pass