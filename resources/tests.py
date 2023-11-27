from django.db import DataError
from django.test import TestCase

# Create your tests here.
from django.test import TestCase
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
        # Continue asserting other fields...

    def test_max_length_constraints(self):
        # Test max_length constraints of fields
        long_string = 'x' * 200  # A string longer than any max_length in the model
        with self.assertRaises(DataError):
            Resource.objects.create(name=long_string)

    def test_nullable_fields(self):
        # Test nullable fields
        resource = Resource.objects.create(name='Test Resource')
        self.assertIsNone(resource.category)
        self.assertIsNone(resource.description)
        # Continue testing other nullable fields...
