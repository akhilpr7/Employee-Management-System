from rest_framework import serializers
from .models import FormTemplate, FormField, Employee, EmployeeFieldValue


class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ("id", "label", "field_type", "placeholder", "is_required", "order", "options")


class FormTemplateSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True)
    field_count = serializers.ReadOnlyField()
    created_by_name = serializers.StringRelatedField(source="created_by")

    class Meta:
        model = FormTemplate
        fields = ("id", "name", "description", "fields", "field_count", "created_by_name", "created_at", "updated_at")
        read_only_fields = ("id", "created_by_name", "created_at", "updated_at")

    def create(self, validated_data):
        fields_data = validated_data.pop("fields", [])
        form = FormTemplate.objects.create(**validated_data)
        for idx, field_data in enumerate(fields_data):
            field_data.setdefault("order", idx)
            FormField.objects.create(form=form, **field_data)
        return form

    def update(self, instance, validated_data):
        fields_data = validated_data.pop("fields", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if fields_data is not None:
            instance.fields.all().delete()
            for idx, field_data in enumerate(fields_data):
                field_data.setdefault("order", idx)
                FormField.objects.create(form=instance, **field_data)
        return instance


class FormTemplateListSerializer(serializers.ModelSerializer):
    field_count = serializers.ReadOnlyField()

    class Meta:
        model = FormTemplate
        fields = ("id", "name", "description", "field_count", "created_at")


# ── Employee ────────────────────────────────────────────────────────────────

class EmployeeFieldValueSerializer(serializers.ModelSerializer):
    field_label = serializers.ReadOnlyField(source="field.label")
    field_type = serializers.ReadOnlyField(source="field.field_type")

    class Meta:
        model = EmployeeFieldValue
        fields = ("id", "field", "field_label", "field_type", "value")


class EmployeeSerializer(serializers.ModelSerializer):
    field_values = EmployeeFieldValueSerializer(many=True, read_only=True)
    display_name = serializers.SerializerMethodField()
    form_template_name = serializers.ReadOnlyField(source="form_template.name")
    values = serializers.DictField(
        child=serializers.CharField(allow_blank=True),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Employee
        fields = (
            "id", "form_template", "form_template_name",
            "field_values", "display_name",
            "values", "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def get_display_name(self, obj):
        return obj.get_display_name()

    def _save_values(self, employee, values: dict):
        for field_id, value in values.items():
            try:
                field = employee.form_template.fields.get(pk=int(field_id))
            except (FormField.DoesNotExist, ValueError):
                continue
            EmployeeFieldValue.objects.update_or_create(
                employee=employee, field=field, defaults={"value": value}
            )

    def create(self, validated_data):
        values = validated_data.pop("values", {})
        employee = Employee.objects.create(**validated_data)
        self._save_values(employee, values)
        return employee

    def update(self, instance, validated_data):
        values = validated_data.pop("values", {})
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        self._save_values(instance, values)
        return instance


class EmployeeListSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    form_template_name = serializers.ReadOnlyField(source="form_template.name")
    data = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ("id", "form_template", "form_template_name", "display_name", "data", "created_at")

    def get_display_name(self, obj):
        return obj.get_display_name()

    def get_data(self, obj):
        return obj.to_dict()
