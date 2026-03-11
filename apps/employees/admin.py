from django.contrib import admin
from .models import FormTemplate, FormField, Employee, EmployeeFieldValue


class FormFieldInline(admin.TabularInline):
    model = FormField
    extra = 0
    fields = ("label", "field_type", "is_required", "order")


@admin.register(FormTemplate)
class FormTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "field_count", "created_by", "created_at")
    inlines = [FormFieldInline]
    search_fields = ("name",)


class EmployeeFieldValueInline(admin.TabularInline):
    model = EmployeeFieldValue
    extra = 0
    readonly_fields = ("field",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("__str__", "form_template", "created_by", "created_at")
    list_filter = ("form_template",)
    inlines = [EmployeeFieldValueInline]
    readonly_fields = ("created_at", "updated_at")
