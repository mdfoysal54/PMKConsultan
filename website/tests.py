from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import Inquiry, SiteSettings


class PublicTests(TestCase):
    def test_pages(self):
        page_names = ['home', 'services', 'about', 'work', 'contact', 'health']
        for name in page_names:
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_csrf_protected(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse('contact'), {'name': 'Test'})
        self.assertEqual(response.status_code, 403)

    def test_valid_inquiry(self):
        payload = {
            'name': 'Test Client',
            'email': 'client@example.com',
            'company': 'Example',
            'service': 'website',
            'budget': '',
            'details': 'Please build our new company website.',
        }
        response = self.client.post(reverse('contact'), payload)
        self.assertRedirects(response, reverse('contact_success'))
        self.assertEqual(Inquiry.objects.count(), 1)

    def test_honeypot(self):
        payload = {
            'name': 'Test Client',
            'email': 'client@example.com',
            'company': 'Example',
            'service': 'website',
            'budget': '',
            'details': 'Please build our website.',
            'website': 'spam.example',  # Honeypot field filled by bot
        }
        self.client.post(reverse('contact'), payload)
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_settings_singleton_update(self):
        """Verify that updating the singleton updates pk=1 without creating duplicates."""
        settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
        settings_obj.company_name = 'PMK Updated'
        settings_obj.save()

        refetched = SiteSettings.objects.get(pk=1)
        self.assertEqual(refetched.company_name, 'PMK Updated')
        self.assertEqual(SiteSettings.objects.count(), 1)

    def test_settings_singleton_duplicate_prevention(self):
        """Verify the singleton behavior when attempting to create a second instance."""
        SiteSettings.objects.get_or_create(pk=1, defaults={'company_name': 'PMK'})

        # If your SiteSettings model overrides save() to lock pk=1:
        second_instance = SiteSettings(company_name='PMK Secondary')
        second_instance.save()

        self.assertEqual(SiteSettings.objects.count(), 1)
        self.assertEqual(SiteSettings.objects.get(pk=1).company_name, 'PMK Secondary')