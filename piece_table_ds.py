class Chunk:
    def __init__(self, text=""):
        self.text = list(text)  # Store text as a list of characters
        self.next = None        # Pointer to the next chunk
        self.prev = None        # Pointer to the previous chunk

    def __len__(self):
        return len(self.text)

    def __repr__(self):
        return ''.join(self.text)


class LinkedListOfChunks:
    def __init__(self, chunk_size=100):
        self.chunk_size = chunk_size  # Max size of each chunk
        self.head = Chunk()           # Start with an empty chunk
        self.tail = self.head

    def insert(self, position, text):
        """Insert text at a specific position in the linked list of chunks."""
        chunk, local_pos = self.find_chunk(position)

        # Insert each character
        for char in text:
            if len(chunk) < self.chunk_size:
                chunk.text.insert(local_pos, char)
            else:
                # Split the chunk if it's full
                new_chunk = Chunk(chunk.text[local_pos:])
                chunk.text = chunk.text[:local_pos]
                new_chunk.next = chunk.next
                new_chunk.prev = chunk
                if new_chunk.next:
                    new_chunk.next.prev = new_chunk
                else:
                    self.tail = new_chunk
                chunk.next = new_chunk

                # Insert the character into the appropriate chunk
                if len(chunk) < self.chunk_size:
                    chunk.text.append(char)
                else:
                    new_chunk.text.insert(0, char)

                chunk = new_chunk
                local_pos = 0

            local_pos += 1

    def delete(self, position, length):
        """Delete a range of characters from the linked list of chunks."""
        chunk, local_pos = self.find_chunk(position)

        while length > 0 and chunk:
            delete_count = min(length, len(chunk) - local_pos)
            del chunk.text[local_pos:local_pos + delete_count]
            length -= delete_count

            if len(chunk) == 0 and chunk.prev and chunk.next:
                # Remove empty chunk
                chunk.prev.next = chunk.next
                chunk.next.prev = chunk.prev
                if chunk == self.tail:
                    self.tail = chunk.prev

            chunk = chunk.next
            local_pos = 0

    def find_chunk(self, position):
        """Find the chunk and local position for a given character position."""
        chunk = self.head
        while chunk and position >= len(chunk):
            position -= len(chunk)
            chunk = chunk.next
        return chunk, position

    def get_text(self):
        """Retrieve the full text of the document."""
        text = []
        chunk = self.head
        while chunk:
            text.append(''.join(chunk.text))
            chunk = chunk.next
        return ''.join(text)

    def display_chunks(self):
        """Display the chunks in the linked list."""
        chunks = []
        chunk = self.head
        while chunk:
            chunks.append(f"[{''.join(chunk.text)}]")
            chunk = chunk.next
        return ' -> '.join(chunks)


# Testing the LinkedListOfChunks Implementation

# Create a linked list of chunks with a smaller chunk size for testing
document = LinkedListOfChunks(chunk_size=10)

# Initial state
print("Initial document:", document.get_text())
print("Chunks:", document.display_chunks())

# Test Insertion
document.insert(0, "Hello world!")
print("\nAfter inserting 'Hello world!':")
print("Document:", document.get_text())
print("Chunks:", document.display_chunks())

# Insert more text to test chunk splitting
document.insert(5, " beautiful")
print("\nAfter inserting ' beautiful' at position 5:")
print("Document:", document.get_text())
print("Chunks:", document.display_chunks())

# Test Deletion
document.delete(5, 10)  # Delete " beautiful"
print("\nAfter deleting ' beautiful':")
print("Document:", document.get_text())
print("Chunks:", document.display_chunks())

# Insert text at the beginning
document.insert(0, "Start-")
print("\nAfter inserting 'Start-' at the beginning:")
print("Document:", document.get_text())
print("Chunks:", document.display_chunks())

# Insert text at the end
document.insert(len(document.get_text()), "!!!")
print("\nAfter inserting '!!!' at the end:")
print("Document:", document.get_text())
print("Chunks:", document.display_chunks())

# Delete text from the middle
document.delete(6, 5)  # Delete "Hello"
print("\nAfter deleting 'Hello' from the middle:")
print("Document:", document.get_text())
print("Chunks:", document.display_chunks())

# Final display of the document
print("\nFinal Document:", document.get_text())
print("Final Chunks:", document.display_chunks())
