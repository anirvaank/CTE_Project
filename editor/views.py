from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Document
import json

@csrf_exempt
def create_document(request):
    """
    API to create a new document.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        name = data.get("name")
        if not name:
            return JsonResponse({"error": "Name is required"}, status=400)

        if Document.objects.filter(name=name).exists():
            return JsonResponse({"error": "Document already exists"}, status=400)

        doc = Document.objects.create(name=name, content="")
        return JsonResponse({"message": "Document created", "id": doc.id, "name": doc.name})

    return JsonResponse({"error": "Method not allowed"}, status=405)

# @csrf_exempt
# def fetch_document(request, document_id):
#     """
#     API to fetch the content of a document by ID.
#     """
#     if request.method == "GET":
#         doc = get_object_or_404(Document, id=document_id)
#         return JsonResponse({"id": doc.id, "name": doc.name, "content": doc.content})

#     return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def update_document(request, document_id):
    """
    API to update a document using insert or delete operations.
    """
    if request.method == "POST":
        doc = get_object_or_404(Document, id=document_id)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        operation = data.get("operation")
        position = data.get("position")

        if operation == "insert":
            text = data.get("text")
            doc.content = doc.content[:position] + text + doc.content[position:]
        elif operation == "delete":
            length = data.get("length")
            doc.content = doc.content[:position] + doc.content[position + length:]
        else:
            return JsonResponse({"error": "Invalid operation"}, status=400)

        doc.save()
        return JsonResponse({"message": "Document updated", "content": doc.content})

    return JsonResponse({"error": "Method not allowed"}, status=405)

from django.http import JsonResponse
from .models import Document

def list_documents(request):
    if request.method == "GET":
        documents = Document.objects.all()
        data = [{"id": doc.id, "name": doc.name, "last_modified": doc.last_modified} for doc in documents]
        return JsonResponse({"documents": data})

    return JsonResponse({"error": "Method not allowed"}, status=405)

def fetch_document(request, document_id):
    if request.method == "GET":
        doc = get_object_or_404(Document, id=document_id)
        return JsonResponse({"id": doc.id, "name": doc.name, "content": doc.content})

from django.http import JsonResponse
from django.shortcuts import render
from .models import Document

def editor_home(request):
    """
    View to display all documents or a welcome message at /editor/.
    """
    if request.method == "GET":
        # Option 1: Render a welcome message
        # return JsonResponse({"message": "Welcome to the Editor API"})

        # Option 2: Display all documents
        documents = Document.objects.all()
        data = [{"id": doc.id, "name": doc.name, "last_modified": doc.last_modified} for doc in documents]
        return JsonResponse({"documents": data})

    return JsonResponse({"error": "Method not allowed"}, status=405)


from django.shortcuts import render, get_object_or_404
from .models import Document

def document_detail(request, document_id):
    """
    Fetch and render a specific document.
    """
    # Fetch the document from the database or return a 404 if not found
    doc = get_object_or_404(Document, id=document_id)
    
    # Render the document in the template
    return render(request, "editor/document_detail.html", {"document": doc})

from django.shortcuts import render
from .models import Document

def list_documents(request):
    """
    View to list all documents.
    """
    documents = Document.objects.all()  # Fetch all documents from the database
    return render(request, "editor/document_list.html", {"documents": documents})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def fetch_document(request, document_id):
    """
    API view to fetch a specific document by ID.
    """
    if request.method == "GET":
        document = get_object_or_404(Document, id=document_id)
        return JsonResponse({
            "id": document.id,
            "name": document.name,
            "content": document.content,
            "last_modified": document.last_modified,
        })
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, get_object_or_404
from .models import Document

def document_detail(request, document_id):
    """
    View to render the details of a specific document.
    """
    document = get_object_or_404(Document, id=document_id)
    return render(request, "editor/document_detail.html", {"document": document})
