from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import FormTemplate, Employee
from .serializers import (
    FormTemplateSerializer,
    FormTemplateListSerializer,
    EmployeeSerializer,
    EmployeeListSerializer,
)


class FormTemplateViewSet(viewsets.ModelViewSet):

    queryset = FormTemplate.objects.prefetch_related("fields").all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return FormTemplateListSerializer
        return FormTemplateSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["get"])
    def fields(self, request, pk=None):
        """Quick endpoint to fetch just the fields of a form."""
        form = self.get_object()
        from .serializers import FormFieldSerializer
        serializer = FormFieldSerializer(form.fields.all(), many=True)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["form_template"]
    search_fields = ["field_values__value"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return (
            Employee.objects.select_related("form_template", "created_by")
            .prefetch_related("field_values__field")
            .all()
        )

    def get_serializer_class(self):
        if self.action == "list":
            return EmployeeListSerializer
        return EmployeeSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=["get"])
    def by_form(self, request):
        form_id = request.query_params.get("form_template")
        if not form_id:
            return Response({"error": "form_template param required."}, status=status.HTTP_400_BAD_REQUEST)
        qs = self.get_queryset().filter(form_template_id=form_id)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = EmployeeListSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        serializer = EmployeeListSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)
