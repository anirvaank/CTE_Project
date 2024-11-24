from editor.piece_table import PieceTable

print("Starting Comprehensive Piece Table Tests...")

def test_piece_table():
    print("Initializing Piece Table...")
    pt = PieceTable("Hello World")
    assert pt.get_content() == "Hello World", "Initial content mismatch."
    print("Test 1 Passed: Initial content is correct.")

    # Test insertion
    print("Testing insertion...")
    pt.insert(6, "Beautiful ")
    assert pt.get_content() == "Hello Beautiful World", "Insertion failed."
    print("Test 2 Passed: Insertion works correctly.")

    # Test deletion
    print("Testing deletion...")
    pt.delete(6, 10)
    assert pt.get_content() == "Hello World", "Deletion failed."
    print("Test 3 Passed: Deletion works correctly.")

    # Test insertion at the beginning
    print("Testing insertion at the beginning...")
    pt.insert(0, "Start-")
    assert pt.get_content() == "Start-Hello World", "Insertion at beginning failed."
    print("Test 4 Passed: Insertion at the beginning works.")

    # Test deletion at the beginning
    print("Testing deletion at the beginning...")
    pt.delete(0, 6)
    assert pt.get_content() == "Hello World", "Deletion at beginning failed."
    print("Test 5 Passed: Deletion at the beginning works.")

    # Test inserting at the end
    print("Testing insertion at the end...")
    pt.insert(pt.length(), "!!!")
    assert pt.get_content() == "Hello World!!!", "Insertion at the end failed."
    print("Test 6 Passed: Insertion at the end works.")

    # Test deleting the last character
    print("Testing deletion of the last character...")
    pt.delete(pt.length() - 3, 3)
    assert pt.get_content() == "Hello World", "Deletion at the end failed."
    print("Test 7 Passed: Deletion of the last character works.")

    # Test complex sequence of operations
    print("Testing complex sequence of operations...")
    pt.insert(5, " Everyone")
    print(f"After inserting ' Everyone': {pt.get_content()}")
    pt.delete(0, 6)  # Delete "Hello "
    print(f"After deleting 'Hello ': {pt.get_content()}")
    pt.insert(0, "Greetings, ")
    print(f"After inserting 'Greetings, ': {pt.get_content()}")
    assert pt.get_content() == "Greetings, Everyone World", "Complex sequence failed."
    print("Test 8 Passed: Complex sequence of operations works.")

if __name__ == "__main__":
    test_piece_table()
