from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from tasks.models import TaskType, Task

TASKS_URL = reverse("tasks:tasks-list")


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
