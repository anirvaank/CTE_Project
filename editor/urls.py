from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_documents, name="list_documents"),  # List all documents
    path("<int:document_id>/", views.fetch_document, name="fetch_document"),  # Fetch a specific document
    path("create/", views.create_document, name="create_document"),  # Create a document
    path("<int:document_id>/update/", views.update_document, name="update_document"),  # Update a document
]
