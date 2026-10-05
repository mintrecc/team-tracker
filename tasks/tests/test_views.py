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


class TaskTypeDetailViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="secretpassword"
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Test task for type",
            description="Testing task type relations",
            priority=Task.Priority.MEDIUM,
            task_type=self.task_type,
        )
        self.detail_url = reverse(
            "tasks:task-type-detail",
            kwargs={"pk": self.task_type.pk}
        )

    def test_task_type_detail_view_status_code_and_template(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_type_detail.html")

    def test_task_type_detail_context_and_related_tasks(self):
        response = self.client.get(self.detail_url)
        self.assertIn("task_type_detail", response.context)

        task_type_in_context = response.context["task_type_detail"]
        self.assertEqual(task_type_in_context, self.task_type)


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
