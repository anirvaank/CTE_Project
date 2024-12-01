from django.db import models
import json

class Document(models.Model):
    """
    Model to represent a collaborative document with Piece Table integration.
    """
    name = models.CharField(max_length=255, unique=True, default="Untitled Document")  # Document name (unique)
    content = models.TextField(default="", blank=True)  # Redundant field for convenience
    original_buffer = models.TextField(default="", blank=True)  # Original buffer storage
    add_buffer = models.TextField(default="", blank=True)  # Add buffer storage
    pieces = models.TextField(default="[]", blank=True)  # JSON representation of the piece table's pieces

    last_modified = models.DateTimeField(auto_now=True)  # Auto-updated timestamp

    def save_piece_table(self, piece_table):
        """
        Save the Piece Table data to the model fields.
        :param piece_table: Instance of the Piece Table.
        """
        self.original_buffer = piece_table.original_buffer
        self.add_buffer = piece_table.add_buffer
        self.pieces = json.dumps(piece_table.pieces)
        self.content = piece_table.get_content()  # Optional for convenience
        self.save()

    def load_piece_table(self):
        """
        Load the Piece Table data from the model fields.
        :return: An instance of the Piece Table.
        """
        from editor.piece_table import PieceTable  # Import locally to avoid circular imports
        piece_table = PieceTable(self.original_buffer)
        piece_table.add_buffer = self.add_buffer
        piece_table.pieces = json.loads(self.pieces)
        return piece_table

