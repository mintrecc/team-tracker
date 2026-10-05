from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.forms import WorkerCreationForm
from tasks.models import Position


class RegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_model = get_user_model()
        cls.position = Position.objects.create(name="Developer")
        cls.register_url = reverse("register")

    def test_register_page_accessible_by_anonymous_user(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_register_page_uses_correct_form(self):
        response = self.client.get(self.register_url)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], WorkerCreationForm)

    def test_register_success_creates_user_and_hashes_password(self):
        initial_user_count = self.user_model.objects.count()
        form_data = {
            "username": "new_developer",
            "first_name": "Alex",
            "last_name": "Smith",
            "position": self.position.pk,
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }

        response = self.client.post(self.register_url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.user_model.objects.count(),
            initial_user_count + 1
        )

        created_user = self.user_model.objects.get(username="new_developer")
        self.assertEqual(created_user.first_name, "Alex")
        self.assertEqual(created_user.last_name, "Smith")
        self.assertEqual(created_user.position, self.position)
        self.assertTrue(created_user.check_password("StrongPass123!"))

    def test_register_auto_logs_in_user(self):
        form_data = {
            "username": "auto_logged_user",
            "first_name": "John",
            "last_name": "Doe",
            "position": self.position.pk,
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }

        self.client.post(
            self.register_url,
            data=form_data
        )

        user = self.user_model.objects.get(username="auto_logged_user")
        self.assertEqual(
            int(self.client.session.get("_auth_user_id")),
            user.pk
        )

    def test_register_password_mismatch_fails(self):
        initial_user_count = self.user_model.objects.count()
        form_data = {
            "username": "mismatch_user",
            "position": self.position.pk,
            "password1": "PasswordOne123!",
            "password2": "PasswordTwo123!",
        }

        response = self.client.post(self.register_url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user_model.objects.count(), initial_user_count)
        self.assertFormError(
            response.context["form"],
            "password2",
            "The two password fields didn’t match.",
        )

    def test_register_duplicate_username_fails(self):
        self.user_model.objects.create_user(
            username="existing_user",
            password="somepassword123",
        )
        initial_user_count = self.user_model.objects.count()

        form_data = {
            "username": "existing_user",
            "position": self.position.pk,
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }

        response = self.client.post(self.register_url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user_model.objects.count(), initial_user_count)
        self.assertFormError(
            response.context["form"],
            "username",
            "A user with that username already exists.",
        )
