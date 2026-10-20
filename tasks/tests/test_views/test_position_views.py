from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from tasks.models import Position

POSITION_URL = reverse("tasks:positions-list")


class PositionListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Position.objects.bulk_create(
            [Position(name=f"testPosition{i}") for i in range(1, 6)]
        )

    def setUp(self):
        self.user_model = get_user_model()

        self.user = self.user_model.objects.create_user(
            username="registered_worker",
            password="secretpassword123",
            email="email@example.com",
            first_name="John",
            last_name="Doe",
        )

        self.client.force_login(self.user)

    def test_retrieve_worker(self):
        response = self.client.get(POSITION_URL)
        self.assertEqual(response.status_code, 200)
        workers = Position.objects.all()
        self.assertQuerySetEqual(
            response.context["position_list"],
            workers.order_by("name")
        )
        self.assertTemplateUsed(response, "tasks/positions_list.html")


class PositionDetailView(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Project Manager")
        self.user = get_user_model().objects.create_user(
            username="manager_test",
            password="secretpassword123",
            first_name="Alice",
            last_name="Smith",
            position=self.position,
        )
        self.detail_url = reverse(
            "tasks:position-detail",
            kwargs={"pk": self.position.pk}
        )
        self.client.force_login(self.user)

    def test_position_detail_status_and_template(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/position_detail.html")

    def test_position_detail_context_and_workers(self):
        response = self.client.get(self.detail_url)
        self.assertIn("position", response.context)

        position = response.context["position"]
        self.assertEqual(position, self.position)

        workers_rel = getattr(position, "workers", None) or position.worker_set
        self.assertIn(self.user, workers_rel.all())

        self.assertContains(response, self.position.name)
        self.assertContains(response, self.user.username)


class PositionCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_user",
            password="secretpassword123",
        )
        self.create_url = reverse("tasks:position-create")

        self.client.force_login(self.user)

    def test_position_create_view_get_template_and_form(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/position_form.html")
        self.assertIn("form", response.context)

    def test_position_create_post_success(self):
        initial_count = Position.objects.count()
        form_data = {"name": "Product Owner"}

        response = self.client.post(self.create_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Position.objects.count(), initial_count + 1)
        self.assertTrue(Position.objects.filter(name="Product Owner").exists())

    def test_position_create_post_invalid_data_missing_name(self):
        initial_count = Position.objects.count()
        form_data = {"name": ""}

        response = self.client.post(self.create_url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Position.objects.count(), initial_count)
        self.assertFormError(
            response.context["form"],
            "name",
            "This field is required.",
        )


class PositionDeleteTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.delete_url = reverse(
            "tasks:position-delete",
            kwargs={"pk": self.position.pk},
        )
        self.user = get_user_model().objects.create_user(
            username="manager_test",
            password="secretpassword123",
            first_name="Alice",
            last_name="Smith",
        )
        self.client.force_login(self.user)

    def test_status_confirmation_delete_page(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "tasks/position_confirm_delete.html"
        )

    def test_delete_work(self):
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
