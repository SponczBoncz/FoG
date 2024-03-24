# from django.contrib.auth import get_user_model
# from django.test import TestCase
# # from django.test.client import Client
# # from django.urls import reverse
# # from django.contrib.auth.models import User
# # from django.contrib.auth import authenticate, login, logout
# # from django.contrib.messages.middleware import MessageMiddleware
# # from django.contrib.sessions.middleware import SessionMiddleware
# # from django.test import RequestFactory
# #
# # from .models import Game, Category, GameMechanic, RequestedCategory, RequestedMechanic, STATUS_CHOICES
# # from .forms import LoginForm, UserCreationForm
# #
# # from .views import LoginView, LogoutView, UserCreationView, UserCollectionView, AddGameToCollectionView, DeleteGameFromCollectionView
#
#
#
# class UsersManagersTests(TestCase):
#
#     def test_create_user(self):
#         User = get_user_model()
#         user = User.objects.create_user(email="normal@user.com", password="foo")
#         self.assertEqual(user.email, "normal@user.com")
#         # self.assertTrue(user.is_active)
#         # self.assertFalse(user.is_staff)
#         self.assertFalse(user.admin)
#         try:
#             # username is None for the AbstractUser option
#             # username does not exist for the AbstractBaseUser option
#             self.assertIsNone(user.username)
#         except AttributeError:
#             pass
#         with self.assertRaises(TypeError):
#             User.objects.create_user()
#         with self.assertRaises(TypeError):
#             User.objects.create_user(email="")
#         with self.assertRaises(ValueError):
#             User.objects.create_user(email="", password="foo")
#
# # class LoginViewTests(TestCase):
# #
# #     def test_login_view(client):
# #         # Create a test user
# #         user = User.objects.create_user(username='testuser', password='testtesttesttest')
# #
# #         # Make a POST request to login
# #         response = client.post(reverse('login'), {'username': 'testuser', 'password': 'testtesttesttest'})
# #
# #         # Assert that the response redirects to 'all-games' page upon successful login
# #         assert response.status_code == 302
# #         assert response.url == reverse('all-games')
# #
# #         # Assert that the user is logged in
# #         assert '_auth_user_id' in client.session
#
#
# class UserCreationViewTests(TestCase):
#     def test_user_creation_view(client):
#         # Make a POST request to register a new user
#         response = client.post(reverse('user-creation'), {
#             'username': 'newuser',
#             'password1': 'testpassword123',
#             'password2': 'testpassword123'
#         })
#
#         # Assert that the response redirects to 'login' page upon successful user creation
#         assert response.status_code == 302
#         assert response.url == reverse('login')
#
#         # Assert that the new user is created in the database
#         assert User.objects.filter(username='newuser').exists()

#
# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from django.test.client import RequestFactory
# from userbase.views import LuckyShotView
# from userbase.forms import LuckyShotForm
#
#
# User = get_user_model()
#
# class LuckyShotViewTest(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
#
#     def test_get_method(self):
#         request = self.factory.get(reverse('lucky-shot'))
#         request.user = self.user
#         response = LuckyShotView.as_view()(request)
#         self.assertEqual(response.status_code, 200)
#
#     def test_post_method_with_valid_form(self):
#         request = self.factory.post(reverse('lucky-shot'), {'no_players': 2})
#         request.user = self.user
#         response = LuckyShotView.as_view()(request)
#         self.assertEqual(response.status_code, 200)  # Assuming the form is always valid in this test scenario
#
#     def test_post_method_with_invalid_form(self):
#         request = self.factory.post(reverse('lucky-shot'), {})
#         request.user = self.user
#         response = LuckyShotView.as_view()(request)
#         self.assertEqual(response.status_code, 200)  # Assuming the form is always invalid in this test scenario



# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404
# from django.http import HttpRequest
# from django.test.client import RequestFactory
# from userbase.views import UserCreationView, AddGameToCollectionView
# from userbase.forms import UserCreationForm
# from gamelist.models import Game
#
# User = get_user_model()
#
# class UserCreationViewTest(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#
#     def test_form_valid(self):
#         form_data = {
#             'nick': 'testuser',
#             'email': 'test@example.com',
#             'password1': 'testpassword',
#             'password2': 'testpassword',
#         }
#         request = self.factory.post(reverse('register'), data=form_data)
#         response = UserCreationView.as_view()(request)
#         self.assertEqual(response.status_code, 302)  # Check if the user is redirected after successful form submission
#         self.assertTrue(User.objects.filter(email='test@example.com').exists())  # Check if the user is created
#
#
#
# class AddGameToCollectionViewTest(TestCase):
#     def setUp(self):
#         # Create a user
#         self.user_model = get_user_model()
#         self.user = self.user_model.objects.create_user(
#             nick = 'testuser',  # username as a positional argument
#             email='test@example.com',
#             password1='testpassword'
#             password2='testpassword'
#         )
#
#         # Create a game
#         self.game = Game.objects.create(
#             title='Test Game',
#             author='Test Author',
#             description='Test Description',
#             min_players=2,
#             max_players=4,
#             game_time='30 minutes'
#         )
#
#     def test_add_game_to_collection(self):
#         # Log in as the test user
#         self.client.login(username='testuser', password='testpassword')
#
#         # Get the URL for adding a game to the collection
#         url = reverse('add-to-collection', kwargs={'game_pk': self.game.pk})
#
#         # Make a POST request to add the game to the collection
#         response = self.client.post(url)
#
#         # Check that the response status code is 302 (redirect)
#         self.assertEqual(response.status_code, 302)
#
#         # Check that the game is added to the user's collection
#         self.assertTrue(self.user.collection.filter(pk=self.game.pk).exists())
#
#     def test_add_game_to_collection_not_logged_in(self):
#         # Get the URL for adding a game to the collection
#         url = reverse('add-to-collection', kwargs={'game_pk': self.game.pk})
#
#         # Make a POST request to add the game to the collection without logging in
#         response = self.client.post(url)
#
#         # Check that the response status code is 302 (redirect to login)
#         self.assertEqual(response.status_code, 302)
#
#         # Check that the game is not added to the user's collection (since the user is not logged in)
#         self.assertFalse(self.user.collection.filter(pk=self.game.pk).exists())


from django.test import TestCase
from django.urls import reverse
from gamelist.forms import AddMechanicForm
from gamelist.models import RequestedMechanic
#
# class AddMechanicFormTest(TestCase):
#     def test_add_mechanic_form_valid(self):
#         # Create a form data dictionary with valid data
#         form_data = {
#             'name': 'Test Mechanic',
#             'description': 'Test Description',
#             'status': 'pending'
#         }
#
#         # Create a form instance with the form data
#         form = AddMechanicForm(data=form_data)
#
#         # Check if the form is valid
#         self.assertTrue(form.is_valid())
#
#     def test_add_mechanic_form_invalid(self):
#         # Create a form data dictionary with invalid data (empty data)
#         form_data = {}
#
#         # Create a form instance with the form data
#         form = AddMechanicForm(data=form_data)
#
#         # Check if the form is invalid
#         self.assertFalse(form.is_valid())
#
#     def test_add_mechanic_form_save(self):
#         # Create a form data dictionary with valid data
#         form_data = {
#             'name': 'Test Mechanic',
#             'description': 'Test Description',
#             'status': 'pending'
#         }
#
#         # Create a form instance with the form data
#         form = AddMechanicForm(data=form_data)
#
#         # Check if the form is valid
#         self.assertTrue(form.is_valid())
#
#         # Save the form data
#         mechanic = form.save()
#
#         # Check if a RequestedMechanic object was created with the form data
#         self.assertIsInstance(mechanic, RequestedMechanic)


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