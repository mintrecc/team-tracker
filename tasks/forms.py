from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from tasks.models import Task


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")

        if deadline and deadline < timezone.now() + timedelta(hours=1):
            raise ValidationError("Deadline must be at least 1 hour from now.")

        return deadline

    class Meta:
        model = Task
        fields = "__all__"


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by name",
            }
        ),
    )
