from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from tasks.models import Position, TaskType, Task

WORKER_URL = reverse("tasks:workers-list")


class WorkerListViewTest(TestCase):
    def setUp(self):
        Worker = get_user_model()
        self.worker1 = Worker.objects.create_user(
            username="test1",
            password="test1234",
        )

        self.worker2 = Worker.objects.create(
            username="test2",
            password="test1234",
        )

        self.worker3 = Worker.objects.create(
            username="name",
            password="test1234",
        )

    def test_retrieve_worker(self):
        response = self.client.get(WORKER_URL)
        self.assertEqual(response.status_code, 200)
        workers = get_user_model().objects.all()
        self.assertQuerySetEqual(
            response.context["worker_list"],
            workers.order_by("username")
        )
        self.assertTemplateUsed(response, "tasks/worker_list.html")


class WorkerDetailViewTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Backend Developer")
        self.worker = get_user_model().objects.create_user(
            username="johndoe",
            password="secretpassword123",
            first_name="John",
            last_name="Doe",
            position=self.position,
        )
        self.task_type = TaskType.objects.create(name="Feature")
        self.task = Task.objects.create(
            name="Implement auth",
            task_type=self.task_type,
            priority=Task.Priority.HIGH,
        )
        self.task.assignees.add(self.worker)

        self.detail_url = reverse(
            "tasks:worker-detail",
            kwargs={"pk": self.worker.pk}
        )

    def test_worker_detail_status_and_template(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_detail.html")
