from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.models import (
    Task,
    TaskType,
    Position
)

INDEX_URL = reverse("tasks:index")
TASKS_URL = reverse("tasks:tasks-list")
TASK_TYPES_URL = reverse("tasks:task-types-list")
WORKER_URL = reverse("tasks:workers-list")
POSITION_URL = reverse("tasks:positions-list")


class IndexViewTest(TestCase):
    def test_retrieve_context(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn("num_tasks", response.context)
        self.assertIn("num_types", response.context)
        self.assertIn("num_workers", response.context)
        self.assertIn("num_positions", response.context)

    def test_index_template_use(self):
        response = self.client.get(INDEX_URL)

        self.assertTemplateUsed(
            response,
            "tasks/index.html"
        )

        self.assertTemplateUsed(
            response,
            "base.html"
        )

    def test_visits_on_site(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.context["num_visits"], 1)

        response = self.client.get(INDEX_URL)
        self.assertEqual(response.context["num_visits"], 2)


class TasksListViewTest(TestCase):
    def setUp(self):
        self.test_type = TaskType.objects.create(
            name="testType"
        )
        self.task = Task.objects.create(
            name="testTask",
            is_completed=True,
            priority=Task.Priority.MEDIUM,
            task_type=self.test_type,
        )

    def test_retrieve_context(self):
        response = self.client.get(TASKS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/tasks_list.html")
        self.assertQuerySetEqual(
            response.context["task_list"],
            Task.objects.all(),
        )


class TaskDetailView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="secretpassword"
        )
        self.assignee = get_user_model().objects.create_user(
            username="developer",
            password="secretpassword",
            first_name="John",
            last_name="Doe",
        )
        self.task_type = TaskType.objects.create(name="Bug")

        self.task = Task.objects.create(
            name="Fix authentication bug",
            description="Detailed issue description",
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
        )
        self.task.assignees.add(self.user)
        self.detail_url = reverse(
            "tasks:task-detail",
            kwargs={"pk": self.task.pk}
        )

    def test_retrieve_context(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_detail.html")
        self.assertIn("task", response.context)


class TaskTypesListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TaskType.objects.bulk_create(
            [TaskType(name=f"testType{i}") for i in range(1, 6)]
        )

    def test_retrieve_context(self):
        response = self.client.get(TASK_TYPES_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_types_list.html")
        self.assertQuerySetEqual(
            response.context["task_types_list"],
            TaskType.objects.all().order_by("name"),
        )


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
