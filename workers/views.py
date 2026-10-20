from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic

from workers.forms import WorkerCreationForm


class RegisterView(generic.CreateView):
    template_name = "registration/register.html"
    form_class = WorkerCreationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 10


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()


class WorkerCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreationForm
    success_url = reverse_lazy("workers:workers-create")

    def test_func(self):
        return self.request.user.is_staff


class WorkerDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("workers:workers-list")

    def test_func(self):
        return self.request.user.is_staff