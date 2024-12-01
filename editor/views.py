from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Document
from .piece_table import PieceTable
import json
from .operational_transform import OperationalTransform


@csrf_exempt
def create_document(request):
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

        # Create a new Piece Table
        piece_table = PieceTable()
        doc = Document(name=name)
        doc.save_piece_table(piece_table)

        return JsonResponse({"message": "Document created", "id": doc.id, "name": doc.name})

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
    API to update a document using insert or delete operations with OT and Piece Table integration.
    """
    if request.method == "POST":
        try:
            doc = get_object_or_404(Document, id=document_id)
            data = json.loads(request.body)
            operation = data.get("operation")
            position = data.get("position")
            ot = OperationalTransform()

            # Extract operation
            if operation == "insert":
                text = data.get("text")
                new_op = {"type": "insert", "position": position, "text": text}
            elif operation == "delete":
                length = data.get("length")
                new_op = {"type": "delete", "position": position, "length": length}
            else:
                return JsonResponse({"error": "Invalid operation"}, status=400)

            # Apply transformation for each operation in the log
            for existing_op in ot.operations:  # Ensure this is iterating over dictionaries
                new_op = ot.transform(new_op, existing_op)

            # Apply the final transformed operation to the Piece Table
            piece_table = PieceTable(doc.content)
            ot.apply(piece_table, new_op)

            # Update document in the database
            doc.content = piece_table.get_content()
            doc.save()

            # Log the operation
            ot.operations.append(new_op)

            return JsonResponse({"message": "Document updated", "content": doc.content})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

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

from django.shortcuts import render, get_object_or_404
from .models import Document

def document_detail(request, document_id):
    """
    Render the document content for viewing.
    """
    document = get_object_or_404(Document, id=document_id)
    return render(request, "editor/document_detail.html", {"document": document})
