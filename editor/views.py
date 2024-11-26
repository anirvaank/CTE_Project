from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Document
from .piece_table import PieceTable
from .operational_transform import OperationalTransform
import json

# Initialize the OT system
ot_system = OperationalTransform()

@csrf_exempt
def create_document(request):
    """
    API to create a new document with Piece Table integration.
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

        # Initialize the Piece Table for the new document
        piece_table = PieceTable()

        # Save the document in the database
        doc = Document.objects.create(name=name, content=piece_table.get_content())

        return JsonResponse({
            "message": "Document created",
            "id": doc.id,
            "name": doc.name,
            "content": doc.content
        })

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def fetch_document(request, document_id):
    """
    API to fetch the content of a document by ID.
    """
    if request.method == "GET":
        doc = get_object_or_404(Document, id=document_id)
        return JsonResponse({
            "id": doc.id,
            "name": doc.name,
            "content": doc.content
        })

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def update_document(request, document_id):
    """
    API to update a document using Piece Table and Operational Transform.
    """
    if request.method == "POST":
        doc = get_object_or_404(Document, id=document_id)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        operation = data.get("operation")
        position = data.get("position")

        # Retrieve the document's Piece Table
        piece_table = PieceTable(initial_text=doc.content)

        if operation == "insert":
            text = data.get("text")
            if text is None:
                return JsonResponse({"error": "Text is required for insert"}, status=400)

            # Apply the operation via OT
            op = {"type": "insert", "position": position, "text": text}
            for existing_op in ot_system.operations:
                op = ot_system.transform(op, existing_op)

            ot_system.apply(piece_table, op)
        elif operation == "delete":
            length = data.get("length")
            if length is None:
                return JsonResponse({"error": "Length is required for delete"}, status=400)

            # Apply the operation via OT
            op = {"type": "delete", "position": position, "length": length}
            for existing_op in ot_system.operations:
                op = ot_system.transform(op, existing_op)

            ot_system.apply(piece_table, op)
        else:
            return JsonResponse({"error": "Invalid operation"}, status=400)

        # Save the updated content back to the database
        doc.content = piece_table.get_content()
        doc.save()

        return JsonResponse({"message": "Document updated", "content": doc.content})

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def list_documents(request):
    """
    API to list all documents.
    """
    if request.method == "GET":
        documents = Document.objects.all()
        return JsonResponse({
            "documents": [
                {"id": doc.id, "name": doc.name, "last_modified": doc.last_modified.isoformat()}
                for doc in documents
            ]
        })

    return JsonResponse({"error": "Method not allowed"}, status=405)
