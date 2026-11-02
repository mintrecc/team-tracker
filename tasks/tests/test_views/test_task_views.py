from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
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
        self.user = get_user_model().objects.create_user(
            username="manager_test",
            password="secretpassword123",
        )
        self.client.force_login(self.user)

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
        self.client.force_login(self.user)

    def test_retrieve_context(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_detail.html")
        self.assertIn("task", response.context)


class TaskCreateViewTest(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="author",
            password="secretpassword123",
        )
        self.assignee = user_model.objects.create_user(
            username="developer",
            password="secretpassword123",
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.create_url = reverse("tasks:task-create")

        self.client.force_login(self.user)

    def test_task_create_view_get_template_and_form(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_form.html")

    def test_task_create_post_success(self):
        valid_deadline = (timezone.now()
                          + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M")
        form_data = {
            "name": "Resolve login issue",
            "description": "Investigate CSRF cookie problem",
            "deadline": valid_deadline,
            "priority": Task.Priority.HIGH,
            "task_type": self.task_type.pk,
            "assignees": [self.assignee.pk],
        }

        response = self.client.post(self.create_url, data=form_data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Task.objects.count(), 1)
        created_task = Task.objects.first()
        self.assertEqual(created_task.name, form_data["name"])
        self.assertEqual(created_task.task_type, self.task_type)
        self.assertIn(self.assignee, created_task.assignees.all())

    def test_task_create_post_invalid_data_missing_name(self):
        form_data = {
            "name": "",
            "description": "Missing name test",
            "priority": Task.Priority.MEDIUM,
            "task_type": self.task_type.pk,
        }

        response = self.client.post(self.create_url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)
        self.assertFormError(
            response.context["form"],
            "name",
            "This field is required."
        )


class TaskDeleteViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_user",
            password="secretpassword123",
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Test task",
            task_type=self.task_type,
        )
        self.delete_url = reverse(
            "tasks:task-delete",
            kwargs={"pk": self.task.pk},
        )
        self.client.force_login(self.user)

    def test_status_confirmation_delete_page(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_confirm_delete.html")
        self.assertIn("task", response.context)

    def test_delete_task(self):
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
