from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Supervisor, User, Phone, Note, Email, Document
import datetime
from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Phone, Email, Note, Document
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import User, Phone, Email, Note, Document

class UserFunctionalityTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(Username='testuser', password='testpassword')
        self.client.force_login(self.user)  # Assuming User model is compatible with Django's authentication system
    def test_add_phone_get(self):
        response = self.client.get(reverse('add_phone'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/add_phone.html')

    def test_add_phone_post(self):
        response = self.client.post(reverse('add_phone'), {'phone': '1234567890'})
        self.assertRedirects(response, '/user/index')
        self.assertTrue(Phone.objects.filter(phone='1234567890').exists())

    def test_delete_phone(self):
        phone = Phone.objects.create(phone_user=self.user, phone='1234567890')
        response = self.client.post(reverse('delete_phone', args=[phone.id]))
        self.assertRedirects(response, '/user/index')
        self.assertFalse(Phone.objects.filter(id=phone.id).exists())

    def test_add_email_get(self):
        response = self.client.get(reverse('add_email'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/add_email.html')

    def test_add_email_post(self):
        response = self.client.post(reverse('add_email'), {'email': 'test@example.com'})
        self.assertRedirects(response, '/user/index')
        self.assertTrue(Email.objects.filter(email='test@example.com').exists())

    def test_add_note_get(self):
        response = self.client.get(reverse('add_note'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/add_note.html')

    def test_add_note_post(self):
        response = self.client.post(reverse('add_note'), {'title': 'Test Title', 'content': 'Test Content'})
        self.assertRedirects(response, '/user/index')
        self.assertTrue(Note.objects.filter(title='Test Title', content='Test Content').exists())


    def test_add_document_get(self):
        response = self.client.get(reverse('add_document'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/add_document.html')

    def test_add_document_post(self):
        document_file = SimpleUploadedFile("test_file.txt", b"file_content", content_type="text/plain")
        response = self.client.post(reverse('add_document'),
                                    {'title': 'Test Document', 'document': document_file, 'type': 'ID'})
        self.assertRedirects(response, '/user/index')
        self.assertTrue(Document.objects.filter(title='Test Document').exists())

    def test_modify_second_password(self):
        response = self.client.post(reverse('modify_second_password'), {'second_password': '123456'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.second_password, '123456')
        self.assertRedirects(response, '/user/index')

    def test_modify_phone_get(self):
        phone = Phone.objects.create(phone_user=self.user, phone='1234567890')
        response = self.client.get(reverse('modify_phone', args=[phone.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/modify_phone.html')

    def test_modify_phone_post(self):
        phone = Phone.objects.create(phone_user=self.user, phone='1234567890')
        response = self.client.post(reverse('modify_phone', args=[phone.id]), {'phone': '0987654321'})
        self.assertRedirects(response, '/user/index')
        phone.refresh_from_db()
        self.assertEqual(phone.phone, '0987654321')

    def test_delete_email_post(self):
        email = Email.objects.create(email_user=self.user, email='test@example.com')
        response = self.client.post(reverse('delete_email', args=[email.id]))
        self.assertRedirects(response, '/user/index')
        self.assertFalse(Email.objects.filter(id=email.id).exists())

    def test_modify_email_get(self):
        email = Email.objects.create(email_user=self.user, email='test@example.com')
        response = self.client.get(reverse('modify_email', args=[email.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/modify_email.html')

    def test_modify_email_post(self):
        email = Email.objects.create(email_user=self.user, email='test@example.com')
        response = self.client.post(reverse('modify_email', args=[email.id]), {'email': 'updated@example.com'})
        self.assertRedirects(response, '/user/index')
        email.refresh_from_db()
        self.assertEqual(email.email, 'updated@example.com')



class SupervisorModelTest(TestCase):
    def test_supervisor_creation(self):
        supervisor = Supervisor.objects.create(name='Alice')
        self.assertEqual(supervisor.name, 'Alice')
        # Test other fields and constraints

class UserModelTest(TestCase):
    def setUp(self):
        self.supervisor = Supervisor.objects.create(name='Bob')

    def test_user_creation(self):
        user = User.objects.create(
            First_Name='John',
            Last_Name='Doe',
            Username='johndoe',
            password='pass1234',
            supervisor=self.supervisor
            # Add other fields
        )
        self.assertEqual(user.First_Name, 'John')
        # Test other fields and constraints

class PhoneModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(Username='userphone', password='pass1234')

    def test_phone_creation(self):
        phone = Phone.objects.create(
            phone_user=self.user,
            phone=1234567890
        )
        self.assertEqual(phone.phone_user, self.user)
        self.assertEqual(phone.phone, 1234567890)
        self.assertTrue(phone.is_active)
        self.assertIsNotNone(phone.created_time)
        self.assertIsNotNone(phone.updated_time)


class NoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(Username='user1', password='pass1234')

    def test_note_creation(self):
        note = Note.objects.create(
            note_user=self.user,
            title='Test Note',
            content='This is a test note.'
        )
        self.assertEqual(note.note_user, self.user)
        self.assertEqual(note.title, 'Test Note')
        self.assertEqual(note.content, 'This is a test note.')
        self.assertTrue(note.is_active)
        self.assertIsNotNone(note.created_time)
        self.assertIsNotNone(note.updated_time)


class EmailModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(Username='user2', password='pass1234')

    def test_email_creation(self):
        email = Email.objects.create(
            email_user=self.user,
            email='test@example.com'
        )
        self.assertEqual(email.email_user, self.user)
        self.assertEqual(email.email, 'test@example.com')
        self.assertTrue(email.is_active)
        self.assertIsNotNone(email.created_time)
        self.assertIsNotNone(email.updated_time)


class DocumentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(Username='user3', password='pass1234')

    def test_document_creation(self):
        document = Document.objects.create(
            document_user=self.user,
            title='Test Document',
            type='ID'
        )
        self.assertEqual(document.document_user, self.user)
        self.assertEqual(document.title, 'Test Document')
        self.assertEqual(document.type, 'ID')
        self.assertTrue(document.is_active)
        self.assertIsNotNone(document.created_time)
        self.assertIsNotNone(document.updated_time)
        self.assertIsNotNone(document.issued_time)
        self.assertIsNotNone(document.expired_time)

    def test_document_type_choices(self):
        document = Document.objects.create(
            document_user=self.user,
            title='Test Passport',
            type='Passport'
        )
        self.assertIn(document.type, [choice[0] for choice in Document.TYPE_CHOICES])

class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(Username='testuser', password='testpassword')
        # Create other necessary objects like Supervisor, Document etc.
    def test_login_view_get(self):
        response = self.client.get(reverse('login_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')

    def test_login_view_post_valid(self):
        # You'll need to hash the password as per your view logic
        response = self.client.post(reverse('login_view'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, '/user/index')

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('login_view'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertTemplateUsed(response, 'user/login.html')
        # You can also check for the presence of your error message in the response

    def test_reg_view_get(self):
        response = self.client.get(reverse('reg_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')

    def test_reg_view_post(self):
        response = self.client.post(reverse('reg_view'), {
            'username': 'newuser',
            'password_1': 'Newpass123',
            'password_2': 'Newpass123',
            'second_password': '123456'
        })
        self.assertRedirects(response, '/user/index')
        self.assertTrue(User.objects.filter(Username='newuser').exists())

    def test_index_view(self):
        # You may need to set up a session or cookie before this test
        response = self.client.get(reverse('index_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/index.html')


