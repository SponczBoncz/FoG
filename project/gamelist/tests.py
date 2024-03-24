from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from gamelist.models import Game, RequestedMechanic
from gamelist.forms import AddMechanicForm
from userbase.models import User


# from django.contrib.auth.models import User
from django.utils import timezone
from gamelist.models import Category, GameMechanic

class AddMechanicFormTest(TestCase):
    def test_add_mechanic_form_valid(self):
        form_data = {
            'name': 'Test Mechanic',
            'description': 'Test Description',
            'status': 0
        }

        form = AddMechanicForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_add_mechanic_form_invalid(self):
        form_data = {}
        form = AddMechanicForm(data=form_data)
        self.assertFalse(form.is_valid(), form.errors)

    def test_add_mechanic_form_save(self):
        form_data = {
            'name': 'Test Mechanic',
            'description': 'Test Description',
            'status': 0
        }

        form = AddMechanicForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        mechanic = form.save()
        self.assertIsInstance(mechanic, RequestedMechanic)



class AddNewCategoryViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create_user(nick='testuser', email='test@example.com', password='testpassword')

    def test_add_new_category_view(self):
        # Log in the test user
        self.client.login(email='test@example.com', password='testpassword')

        # Define the data to be sent in the POST request
        category_data = {
            'name': 'Test Category',
            'description': 'Test Description',
        }

        # Send a POST request to the view with the category data
        response = self.client.post(reverse('add-new-category'), category_data)

        # Check if the category was created successfully (status code 302 for redirect)
        self.assertEqual(response.status_code, 302)

        # Check if the category was added to the database
        self.assertTrue(Category.objects.filter(name='Test Category').exists())

    def test_add_new_category_view_not_logged_in(self):
        # Define the data to be sent in the POST request
        category_data = {
            'name': 'Test Category',
            'description': 'Test Description',
        }

        # Send a POST request to the view without logging in
        response = self.client.post(reverse('add-new-category'), category_data)

        # Check if the user is redirected to the login page (status code 302 for redirect)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

        # Check if the category was not added to the database
        self.assertFalse(Category.objects.filter(name='Test Category').exists())


class AddNewMechanicViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create_user(nick='testuser', email='test@example.com', password='testpassword')

    def test_add_new_mechanic_view(self):
        # Log in the test user
        self.client.login(email='test@example.com', password='testpassword')

        # Define the data to be sent in the POST request
        mechanic_data = {
            'name': 'Test Mechanic',
            'description': 'Test Description',
        }

        # Send a POST request to the view with the mechanic data
        response = self.client.post(reverse('add-new-mechanic'), mechanic_data)

        # Check if the mechanic was created successfully (status code 302 for redirect)
        self.assertEqual(response.status_code, 302)

        # Check if the mechanic was added to the database
        self.assertTrue(GameMechanic.objects.filter(name='Test Mechanic').exists())

    def test_add_new_mechanic_view_not_logged_in(self):
        # Define the data to be sent in the POST request
        mechanic_data = {
            'name': 'Test Mechanic',
            'description': 'Test Description',
        }

        # Send a POST request to the view without logging in
        response = self.client.post(reverse('add-new-mechanic'), mechanic_data)

        # Check if the user is redirected to the login page (status code 302 for redirect)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

        # Check if the mechanic was not added to the database
        self.assertFalse(GameMechanic.objects.filter(name='Test Mechanic').exists())