from django.test import TestCase
from editor.piece_table import PieceTable

class PieceTableTestCase(TestCase):
    def test_piece_table_operations(self):
        # Initialize Piece Table with initial text
        pt = PieceTable("Hello World")
        self.assertEqual(pt.get_content(), "Hello World")

        # Test insertion
        pt.insert(6, "Beautiful ")
        self.assertEqual(pt.get_content(), "Hello Beautiful World")

        # Test deletion
        pt.delete(6, 10)
        self.assertEqual(pt.get_content(), "Hello World")

        # Test edge cases
        pt.insert(0, "Start-")
        self.assertEqual(pt.get_content(), "Start-Hello World")
