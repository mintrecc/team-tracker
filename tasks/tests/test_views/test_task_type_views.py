from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from tasks.models import TaskType, Task

TASK_TYPES_URL = reverse("tasks:task-types-list")


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
