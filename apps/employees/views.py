import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib import messages

from .models import FormTemplate, FormField, Employee, EmployeeFieldValue


# ── Form Template Views ───────────────────────────────────────────────────────

class FormListView(LoginRequiredMixin, View):
    def get(self, request):
        forms = FormTemplate.objects.prefetch_related("fields").all()
        return render(request, "employees/form_list.html", {"forms": forms})


class FormCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "employees/form_builder.html", {"form_obj": None})


class FormEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        form_obj = get_object_or_404(FormTemplate, pk=pk)
        return render(request, "employees/form_builder.html", {"form_obj": form_obj})


class FormSaveView(LoginRequiredMixin, View):

    def post(self, request):
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({"error": "Invalid JSON payload."}, status=400)

        name = data.get("name", "").strip()
        if not name:
            return JsonResponse({"error": "Form name is required."}, status=400)

        fields_data = data.get("fields", [])
        form_id = data.get("id")

        if form_id:
            form_obj = get_object_or_404(FormTemplate, pk=form_id)
            form_obj.name = name
            form_obj.description = data.get("description", "")
            form_obj.save()
            form_obj.fields.all().delete()
        else:
            form_obj = FormTemplate.objects.create(
                name=name,
                description=data.get("description", ""),
                created_by=request.user,
            )

        for idx, field in enumerate(fields_data):
            FormField.objects.create(
                form=form_obj,
                label=field.get("label", f"Field {idx + 1}"),
                field_type=field.get("field_type", "text"),
                placeholder=field.get("placeholder", ""),
                is_required=field.get("is_required", False),
                order=idx,
                options=field.get("options", []),
            )

        return JsonResponse({"id": form_obj.pk, "name": form_obj.name, "message": "Form saved."})


class FormDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        form_obj = get_object_or_404(FormTemplate, pk=pk)
        form_obj.delete()
        return JsonResponse({"message": "Form deleted."})


class FormFieldsView(LoginRequiredMixin, View):

    def get(self, request, pk):
        form_obj = get_object_or_404(FormTemplate, pk=pk)
        fields = list(
            form_obj.fields.values(
                "id", "label", "field_type", "placeholder", "is_required", "order", "options"
            )
        )
        return JsonResponse({"fields": fields})


# ── Employee Views ────────────────────────────────────────────────────────────

class EmployeeListView(LoginRequiredMixin, View):
    def get(self, request):
        forms = FormTemplate.objects.all()
        form_id = request.GET.get("form_template")
        search = request.GET.get("q", "").strip()

        employees = Employee.objects.select_related("form_template").prefetch_related(
            "field_values__field"
        )
        if form_id:
            employees = employees.filter(form_template_id=form_id)
        if search:
            employees = employees.filter(field_values__value__icontains=search).distinct()

        return render(
            request,
            "employees/employee_list.html",
            {
                "employees": employees,
                "forms": forms,
                "selected_form": form_id,
                "search": search,
            },
        )


class EmployeeCreateView(LoginRequiredMixin, View):
    def get(self, request):
        forms = FormTemplate.objects.prefetch_related("fields").all()
        return render(request, "employees/employee_form.html", {"forms": forms, "employee": None})


class EmployeeEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        employee = get_object_or_404(
            Employee.objects.prefetch_related("field_values__field"), pk=pk
        )
        forms = FormTemplate.objects.prefetch_related("fields").all()
        existing = {str(fv.field_id): fv.value for fv in employee.field_values.all()}
        return render(
            request,
            "employees/employee_form.html",
            {"forms": forms, "employee": employee, "existing_values": json.dumps(existing)},
        )


class EmployeeSaveView(LoginRequiredMixin, View):

    def post(self, request):
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({"error": "Invalid JSON payload."}, status=400)

        form_template_id = data.get("form_template")
        if not form_template_id:
            return JsonResponse({"error": "form_template is required."}, status=400)

        form_template = get_object_or_404(FormTemplate, pk=form_template_id)
        employee_id = data.get("id")

        if employee_id:
            employee = get_object_or_404(Employee, pk=employee_id)
        else:
            employee = Employee.objects.create(
                form_template=form_template, created_by=request.user
            )

        values: dict = data.get("values", {})
        for field_id_str, value in values.items():
            try:
                field = form_template.fields.get(pk=int(field_id_str))
            except (FormField.DoesNotExist, ValueError):
                continue
            EmployeeFieldValue.objects.update_or_create(
                employee=employee, field=field, defaults={"value": value}
            )

        return JsonResponse({"id": employee.pk, "message": "Employee saved."})


class EmployeeDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return JsonResponse({"message": "Employee deleted."})
