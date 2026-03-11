from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FieldType(models.TextChoices):
    TEXT = "text", "Text"
    NUMBER = "number", "Number"
    EMAIL = "email", "Email"
    DATE = "date", "Date"
    PASSWORD = "password", "Password"
    TEXTAREA = "textarea", "Textarea"
    CHECKBOX = "checkbox", "Checkbox"
    SELECT = "select", "Select"
    PHONE = "tel", "Phone"
    URL = "url", "URL"


class FormTemplate(models.Model):

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="form_templates"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def field_count(self):
        return self.fields.count()


class FormField(models.Model):

    form = models.ForeignKey(FormTemplate, on_delete=models.CASCADE, related_name="fields")
    label = models.CharField(max_length=200)
    field_type = models.CharField(max_length=20, choices=FieldType.choices, default=FieldType.TEXT)
    placeholder = models.CharField(max_length=200, blank=True)
    is_required = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    options = models.JSONField(
        default=list,
        blank=True,
        help_text="List of options for 'select' field type.",
    )

    class Meta:
        ordering = ["order"]
        unique_together = [("form", "label")]

    def __str__(self):
        return f"{self.form.name} › {self.label} ({self.field_type})"


class Employee(models.Model):

    form_template = models.ForeignKey(
        FormTemplate, on_delete=models.PROTECT, related_name="employees"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="employees_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        first_val = self.field_values.filter(
            field__field_type__in=["text", "email"]
        ).first()
        if first_val:
            return first_val.value
        return f"Employee #{self.pk}"

    def get_display_name(self):
        return str(self)

    def to_dict(self):
        return {fv.field.label: fv.value for fv in self.field_values.select_related("field")}


class EmployeeFieldValue(models.Model):

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="field_values")
    field = models.ForeignKey(FormField, on_delete=models.CASCADE, related_name="values")
    value = models.TextField(blank=True, default="")

    class Meta:
        unique_together = [("employee", "field")]

    def __str__(self):
        return f"{self.employee} › {self.field.label}: {self.value}"
