import hashlib

from django.db import DataError
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
from django.utils import timezone
from datetime import timedelta


# This is a test class to test all user functionality in the User app
class UserFunctionalityTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.supervisor = Supervisor.objects.create(name='Bob')
        self.user = User.objects.create(Username='testuser', password='testpassword', supervisor=self.supervisor)
        session = self.client.session
        session['uid'] = self.user.id
        session.save()
        self.client.force_login(self.user)

    # This is a test function to test the add phone functionality by GET request
    def test_add_phone_get(self):
        response = self.client.get('/user/add_phone')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/add_phone.html')

    # This is a test function to test the add phone functionality by POST request
    def test_add_phone_post(self):
        response = self.client.post('/user/add_phone', {'phone': '1234567890'})
        self.assertRedirects(response, '/user/index')
        self.assertTrue(Phone.objects.filter(phone='1234567890').exists())

    # This is a test function to test the delete phone functionality by GET request
    def test_delete_phone(self):
        phone = Phone.objects.create(phone_user=self.user, phone='213546879')
        response = self.client.post(f'/user/delete_phone/{phone.id}')
        self.assertRedirects(response, '/user/index')
        self.assertFalse(Phone.objects.filter(id=phone.id).exists())

    # This is a test function to test the add email functionality by GET request
    def test_add_email_get(self):
        response = self.client.get('/user/add_email')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/add_email.html')

    # This is a test function to test the add email functionality by POST request
    def test_add_email_post(self):
        response = self.client.post('/user/add_email', {'email': 'test@example.com'})
        self.assertRedirects(response, '/user/index')
        self.assertTrue(Email.objects.filter(email='test@example.com').exists())

    # This is a test function to test the add note functionality by GET request
    def test_add_note_get(self):
        response = self.client.get('/user/add_note')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/add_note.html')

    # This is a test function to test the add note functionality by POST request
    def test_add_note_post(self):
        response = self.client.post('/user/add_note', {'title': 'Test Title', 'content': 'Test Content'})
        self.assertRedirects(response, '/user/index')
        self.assertTrue(Note.objects.filter(title='Test Title', content='Test Content').exists())

    # This is a test function to test the add document functionality by GET request
    def test_add_document_get(self):
        response = self.client.get('/user/add_document')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/add_document.html')

    # This is a test function to test the add document functionality by POST request
    def test_add_document_post(self):
        document_file = SimpleUploadedFile("test_file.txt", b"file_content", content_type="text/plain")
        response = self.client.post('/user/add_document',
                                    {'title': 'Test Document', 'document': document_file, 'type': 'ID'})
        self.assertRedirects(response, '/user/index')
        self.assertTrue(Document.objects.filter(title='Test Document').exists())

    # This is a test function to test the modify second password functionality by POST request
    def test_modify_second_password(self):
        response = self.client.post('/user/modify_second_password', {'second_password': '123456'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.second_password, 123456)
        self.assertRedirects(response, '/user/index')

    # This is a test function to test the modify phone functionality by GET request
    def test_modify_phone_get(self):
        phone = Phone.objects.create(phone_user=self.user, phone='1234567890')
        response = self.client.get(f'/user/modify_phone/{phone.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/modify_phone.html')

    # This is a test function to test the modify phone functionality by POST request
    def test_modify_phone_post(self):
        phone = Phone.objects.create(phone_user=self.user, phone='1234567890')
        response = self.client.post(f'/user/modify_phone/{phone.id}', {'phone': '0987654321'})
        self.assertRedirects(response, '/user/index')
        phone.refresh_from_db()
        self.assertEqual(phone.phone, 987654321)

    # This is a test function to test the delete email functionality by POST request
    def test_delete_email_post(self):
        email = Email.objects.create(email_user=self.user, email='test@example.com')
        response = self.client.post(f'/user/delete_email/{email.id}')
        self.assertRedirects(response, '/user/index')
        self.assertFalse(Email.objects.filter(id=email.id).exists())

    # This is a test function to test the modify email functionality by GET request
    def test_modify_email_get(self):
        email = Email.objects.create(email_user=self.user, email='test@example.com')
        response = self.client.get(f'/user/modify_email/{email.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/modify_email.html')

    # This is a test function to test the modify email functionality by POST request
    def test_modify_email_post(self):
        email = Email.objects.create(email_user=self.user, email='test@example.com')
        response = self.client.post(f'/user/modify_email/{email.id}', {'email': 'updated@example.com'})
        self.assertRedirects(response, '/user/index')
        email.refresh_from_db()
        self.assertEqual(email.email, 'updated@example.com')

    # This is a test function to test the delete note functionality by POST request
    def test_delete_note_post(self):
        note = Note.objects.create(
            note_user=self.user,
            title='Test Note',
            content='This is a test note.'
        )
        response = self.client.post(f'/user/delete_note/{note.id}')
        self.assertRedirects(response, '/user/index')
        self.assertFalse(Note.objects.filter(id=note.id).exists())

    # This is a test function to test the modify note functionality by GET request
    def test_modify_note_get(self):
        note = Note.objects.create(
            note_user=self.user,
            title='Test Note',
            content='This is a test note.'
        )
        response = self.client.get(f'/user/modify_note/{note.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/modify_note.html')

    # This is a test function to test the modify phone functionality by POST request
    def test_modify_note_post(self):
        note = Note.objects.create(
            note_user=self.user,
            title='Test Note',
            content='This is a test note.'
        )
        response = self.client.post(f'/user/modify_note/{note.id}', {'title': 'Test Note1'})
        self.assertRedirects(response, '/user/index')
        note.refresh_from_db()
        self.assertEqual(note.title, 'Test Note1')

    # This is a test function to test the delete document functionality by POST request
    def test_delete_document_post(self):
        document = Document.objects.create(
            document_user=self.user,
            title='Test Document',
            type='ID'
        )
        response = self.client.post(f'/user/delete_document/{document.id}')
        self.assertRedirects(response, '/user/index')
        self.assertFalse(Document.objects.filter(id=document.id).exists())

    # This is a test function to test the modify document functionality by GET request
    def test_modify_document_get(self):
        document = Document.objects.create(
            document_user=self.user,
            title='Test Document',
            type='ID',
            document="1.jpg"
        )
        response = self.client.get(f'/user/modify_document/{document.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/modify_document.html')

    # This is a test function to test the modify document functionality by POST request
    def test_modify_document_post(self):
        document = Document.objects.create(
            document_user=self.user,
            title='Test Document',
            type='ID',
            document="1.jpg"
        )
        response = self.client.post(f'/user/modify_document/{document.id}', {'title': 'Test Document1'})
        self.assertRedirects(response, '/user/index')
        document.refresh_from_db()
        self.assertEqual(document.title, 'Test Document1')

    # This is a test function to test the account view functionality by GET request
    def test_account_view(self):
        response = self.client.get('/user/account')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/account.html')
        self.assertEqual(response.context['user'].id, self.user.id)


# This test class is used to test the Supervisor table in the database
class SupervisorModelTest(TestCase):
    # This test function is used to test create a supervisor functionality
    def test_supervisor_creation(self):
        supervisor = Supervisor.objects.create(name='Alice')
        self.assertEqual(supervisor.name, 'Alice')
        self.assertTrue(supervisor.is_active)
        self.assertTrue(timezone.now() - supervisor.created_time < timedelta(seconds=1))
        self.assertTrue(timezone.now() - supervisor.updated_time < timedelta(seconds=1))
        default_supervisor = Supervisor.objects.create()
        self.assertEqual(default_supervisor.name, 'Zac')

    # This test function is used to test boundary case
    def test_max_length_constraints(self):
        # Test max_length constraints of fields
        short_string = 'x'  # A string longer than any max_length in the model
        with self.assertRaises(DataError):
            Supervisor.objects.create(name=short_string * 31)


# This test class is used to test the User table in the database
class UserModelTest(TestCase):
    def setUp(self):
        self.supervisor = Supervisor.objects.create(name='Bob')

    # This test function is used to test create a user functionality
    def test_user_creation(self):
        user = User.objects.create(
            First_Name='John',
            Last_Name='Doe',
            Username='johndoe',
            password='pass1234',
            supervisor=self.supervisor,
            address='123 st',
            gender='male',
            second_password='1111'
        )
        self.assertEqual(user.First_Name, 'John')
        self.assertEqual(user.Last_Name, 'Doe')
        self.assertEqual(user.Username, 'johndoe')
        self.assertEqual(user.password, 'pass1234')
        self.assertEqual(user.address, '123 st')
        self.assertEqual(user.gender, 'male')
        self.assertEqual(user.second_password, '1111')
        self.assertTrue(user.is_active)
        self.assertTrue(timezone.now() - user.created_time < timedelta(seconds=1))
        self.assertTrue(timezone.now() - user.updated_time < timedelta(seconds=1))
        self.assertTrue(timezone.now() - user.last_access_time < timedelta(seconds=1))

    # This test function is used to test boundary case
    def test_max_length_constraints(self):
        # Test max_length constraints of fields
        short_string = 'x'  # A string longer than any max_length in the model
        with self.assertRaises(DataError):
            User.objects.create(First_Name=short_string * 31)
            User.objects.create(Last_Name=short_string * 31)
            User.objects.create(Username=short_string * 31)
            User.objects.create(password=short_string * 33)
            User.objects.create(address=short_string * 256)
            User.objects.create(gender=short_string * 7)

    # This test function is used to test null case
    def test_nullable_fields(self):
        # Test nullable fields
        user = User.objects.create(Username='johndoe', password='pass1234', supervisor=self.supervisor)
        self.assertIsNone(user.First_Name)
        self.assertIsNone(user.Last_Name)
        self.assertIsNone(user.gender)
        self.assertIsNone(user.second_password)


# This test class is used to test the Phone table in the database
class PhoneModelTest(TestCase):
    def setUp(self):
        self.supervisor = Supervisor.objects.create(name='Bob')
        self.user = User.objects.create(Username='userphone', password='pass1234', supervisor=self.supervisor)

    # This test function is used to test create a phone functionality
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


# This test class is used to test the Note table in the database
class NoteModelTest(TestCase):
    def setUp(self):
        self.supervisor = Supervisor.objects.create(name='Bob')
        self.user = User.objects.create(Username='user1', password='pass1234', supervisor=self.supervisor)

    # This test function is used to test create a note functionality
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
        short_string = 'x'  # A string longer than any max_length in the model
        with self.assertRaises(DataError):
            Note.objects.create(note_user=self.user, title=short_string * 33)


# This test class is used to test the Email table in the database
class EmailModelTest(TestCase):
    def setUp(self):
        self.supervisor = Supervisor.objects.create(name='Bob')
        self.user = User.objects.create(Username='user2', password='pass1234', supervisor=self.supervisor)

    # This test function is used to test create a email functionality
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
        short_string = 'x'  # A string longer than any max_length in the model
        with self.assertRaises(DataError):
            Email.objects.create(email_user=self.user, email=short_string * 31)


# This test class is used to test the Document table in the database
class DocumentModelTest(TestCase):
    def setUp(self):
        self.supervisor = Supervisor.objects.create(name='Bob')
        self.user = User.objects.create(Username='user3', password='pass1234', supervisor=self.supervisor)

    # This test function is used to test create a document functionality
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
        short_string = 'x'  # A string longer than any max_length in the model
        with self.assertRaises(DataError):
            Document.objects.create(document_user=self.user, title=short_string * 33)
            Document.objects.create(type=short_string * 33)

    # This test function is used to test boundary case
    def test_document_type_choices(self):
        document = Document.objects.create(
            document_user=self.user,
            title='Test Passport',
            type='Passport'
        )
        self.assertIn(document.type, [choice[0] for choice in Document.TYPE_CHOICES])


# This test class is used to test user page
class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.supervisor = Supervisor.objects.create(name='Bob')
        password = 'testpassword'
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        self.user = User.objects.create(Username='testuser', password=hashed_password, supervisor=self.supervisor)
        session = self.client.session
        session['uid'] = self.user.id
        session.save()
        self.client.force_login(self.user)

    # This test function is used to test user login functionality using GET request
    def test_login_view_get(self):
        response = self.client.get('/user/login')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')

    # This test function is used to test user login functionality using POST request
    def test_login_view_post_valid(self):
        m = hashlib.md5()
        m.update('testpassword'.encode())
        password_m = m.hexdigest()
        response = self.client.post('/user/login', {
            'username': 'testuser',
            'password': password_m
        })
        self.assertEqual(response.status_code, 200)

    # This test function is used to test user login validation using POST request
    def test_login_view_post_invalid(self):
        response = self.client.post('/user/login', {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertTemplateUsed(response, 'user/login.html')

    # This test function is used to test user registration functionality using GET request
    def test_reg_view_get(self):
        response = self.client.get('/user/register')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')

    # This test function is used to test user main page functionality using GET request
    def test_index_view(self):
        response = self.client.get('/user/index')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/index.html')
