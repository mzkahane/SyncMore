from django.test import TestCase, Client


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    # This function is used to test index view
    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/index.html')

    # This function is used to test contact view GET request
    def test_contact_view_get(self):
        response = self.client.get('/index/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/contact.html')

    # This function is used to test contact view POST request
    def test_contact_view_post(self):
        response = self.client.post('/index/contact/', {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'message': 'Hello'
        })
        self.assertEqual(response.status_code, 302)
