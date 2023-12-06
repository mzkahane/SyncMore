from django.db import DataError
from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from resources.models import Resource


class ResourceModelTest(TestCase):

    def test_create_resource(self):
        # Test creating a complete Resource instance
        resource = Resource.objects.create(
            category='Books',
            name='Django for Beginners',
            description='A comprehensive guide to Django framework.',
            address='123 Django St.',
            phone='1234567890',
            email='info@djangoexample.com',
            website='https://www.djangoforbeginners.com',
            website_nickname='DjangoBeginners'
        )

        self.assertEqual(resource.category, 'Books')
        self.assertEqual(resource.name, 'Django for Beginners')
        self.assertEqual(resource.description, 'A comprehensive guide to Django framework.')
        self.assertEqual(resource.address, '123 Django St.')
        self.assertEqual(resource.phone, '1234567890')
        self.assertEqual(resource.email, 'info@djangoexample.com')
        self.assertEqual(resource.website, 'https://www.djangoforbeginners.com')
        self.assertEqual(resource.website_nickname, 'DjangoBeginners')

    def test_max_length_constraints(self):
        # Test max_length constraints of fields
        short_string = 'x'  # A string longer than any max_length in the model
        with self.assertRaises(DataError):
            Resource.objects.create(category=short_string * 129)
            Resource.objects.create(name=short_string * 129)
            Resource.objects.create(description=short_string * 1025)
            Resource.objects.create(address=short_string * 129)
            Resource.objects.create(phone=short_string * 17)
            Resource.objects.create(email=short_string * 31)
            Resource.objects.create(website=short_string * 51)
            Resource.objects.create(website_nickname=short_string * 51)

    def test_nullable_fields(self):
        # Test nullable fields
        resource = Resource.objects.create(name='Test Resource')
        self.assertIsNone(resource.category)
        self.assertIsNone(resource.description)
        self.assertIsNone(resource.address)
        self.assertIsNone(resource.phone)
        self.assertIsNone(resource.email)
        self.assertIsNone(resource.website)
        self.assertIsNone(resource.website_nickname)


class ResourceViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_resources_view(self):
        response = self.client.get('/resources/index')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resources/resources.html')
