class Chunk:
    def __init__(self, text=""):
        self.text = list(text)  # Store line as a list of characters
        self.next = None        # Pointer to the next line (chunk)
        self.prev = None        # Pointer to the previous line (chunk)

    def __len__(self):
        return len(self.text)

    def __repr__(self):
        return ''.join(self.text)


class LinkedListOfChunks:
    def __init__(self):
        self.head = Chunk()  # Start with an empty line (chunk)
        self.tail = self.head

    def insert_text(self, line_num, position, text):
        """Insert text at a specific line and position within that line."""
        chunk = self.get_line_chunk(line_num)
        if chunk is None:
            print(f"Line {line_num} does not exist.")
            return

        for char in text:
            chunk.text.insert(position, char)
            position += 1

    def delete_text(self, start_line, start_pos, end_line, end_pos):
        """Delete text from a range of lines and positions."""
        current_line = start_line
        chunk = self.get_line_chunk(current_line)
        while chunk and (current_line <= end_line):
            if current_line == start_line:
                # Deleting from the start line
                if start_line == end_line:
                    # Deleting within a single line
                    del chunk.text[start_pos:end_pos]
                else:
                    # Deleting from start_pos to end of start_line
                    del chunk.text[start_pos:]
            elif current_line == end_line:
                # Deleting up to end_pos in end_line
                del chunk.text[:end_pos]
            else:
                # Deleting the entire line in between start_line and end_line
                chunk.text = []

            if len(chunk.text) == 0 and chunk != self.head:
                # Remove empty chunk
                if chunk.prev:
                    chunk.prev.next = chunk.next
                if chunk.next:
                    chunk.next.prev = chunk.prev
                if chunk == self.tail:
                    self.tail = chunk.prev

            chunk = chunk.next
            current_line += 1

    def add_line(self, text=""):
        """Add a new line at the end of the document."""
        new_chunk = Chunk(text)
        self.tail.next = new_chunk
        new_chunk.prev = self.tail
        self.tail = new_chunk

    def get_line_chunk(self, line_num):
        """Retrieve the chunk for a specific line number."""
        current = self.head
        current_line = 0
        while current and current_line < line_num:
            current = current.next
            current_line += 1
        return current

    def get_text(self):
        """Retrieve the full text of the document."""
        text = []
        chunk = self.head
        while chunk:
            text.append(''.join(chunk.text))
            chunk = chunk.next
        return '\n'.join(text)

    def display_chunks(self):
        """Display the lines in the document as chunks."""
        chunks = []
        chunk = self.head
        line_num = 0
        while chunk:
            chunks.append(f"Line {line_num}: [{''.join(chunk.text)}]")
            chunk = chunk.next
            line_num += 1
        return ' -> '.join(chunks)


# Testing the LinkedListOfChunks Implementation

# Create a new document
document = LinkedListOfChunks()

# Add some lines
document.head.text = list("Hello world!")
document.add_line("This is a new line.")
document.add_line("Another line here.")

# Initial document state
print("Initial document:")
print(document.get_text())
print("Chunks:", document.display_chunks())

# Insert text within a line
document.insert_text(1, 5, " beautiful")
print("\nAfter inserting ' beautiful' at line 1, position 5:")
print("Document:", document.get_text())
print("Chunks:", document.display_chunks())

# Delete text within a range
document.delete_text(1, 5, 1, 15)  # Delete " beautiful" in line 1
print("\nAfter deleting ' beautiful' from line 1:")
print("Document:", document.get_text())
print("Chunks:", document.display_chunks())

# Insert text at the start of the first line
document.insert_text(0, 0, "Start-")
print("\nAfter inserting 'Start-' at the beginning of line 0:")
print("Document:", document.get_text())
print("Chunks:", document.display_chunks())

# Insert text at the end of the last line
last_line_num = len(document.get_text().splitlines()) - 1
document.insert_text(last_line_num, len(document.get_line_chunk(last_line_num).text), "!!!")
print("\nAfter inserting '!!!' at the end of the last line:")
print("Document:", document.get_text())
print("Chunks:", document.display_chunks())

# Delete text across multiple lines
document.delete_text(0, 6, 2, 7)  # Delete from "world!" in line 0 to "Another" in line 2
print("\nAfter deleting from line 0, position 6 to line 2, position 7:")
print("Document:", document.get_text())
print("Chunks:", document.display_chunks())
