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
