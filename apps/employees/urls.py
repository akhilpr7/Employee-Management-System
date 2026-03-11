from django.urls import path
from . import views

app_name = "employees"

urlpatterns = [
    # Form builder
    path("forms/", views.FormListView.as_view(), name="form_list"),
    path("forms/create/", views.FormCreateView.as_view(), name="form_create"),
    path("forms/<int:pk>/edit/", views.FormEditView.as_view(), name="form_edit"),
    path("forms/save/", views.FormSaveView.as_view(), name="form_save"),
    path("forms/<int:pk>/delete/", views.FormDeleteView.as_view(), name="form_delete"),
    path("forms/<int:pk>/fields/", views.FormFieldsView.as_view(), name="form_fields"),
    # Employees
    path("", views.EmployeeListView.as_view(), name="list"),
    path("create/", views.EmployeeCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.EmployeeEditView.as_view(), name="edit"),
    path("save/", views.EmployeeSaveView.as_view(), name="save"),
    path("<int:pk>/delete/", views.EmployeeDeleteView.as_view(), name="delete"),
]
