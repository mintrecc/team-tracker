from django.test import TestCase
from django.urls import reverse

from tasks.models import Task, TaskType

INDEX_URL = reverse("tasks:index")
TASKS_URL = reverse("tasks:tasks-list")
TASK_TYPES_URL = reverse("tasks:task-types-list")

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

