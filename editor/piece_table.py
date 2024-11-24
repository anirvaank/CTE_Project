class PieceTable:
    def __init__(self, initial_text=""):
        """
        Initialize the Piece Table with an original buffer and an add buffer.
        :param initial_text: The initial text for the document.
        """
        self.original_buffer = initial_text  # Stores the original content
        self.add_buffer = ""  # Stores all new additions
        self.pieces = [("original", 0, len(initial_text))]  # Piece table entries

    def insert(self, position, text):
        """
        Insert text at a given position.
        :param position: Index in the document where text is inserted.
        :param text: The text to insert.
        """
        print(f"Inserting '{text}' at position {position}...")
        print(f"Before insertion, pieces: {self.pieces}")

        if position < 0 or position > self.length():
            raise ValueError("Insert position out of bounds")

        add_start = len(self.add_buffer)
        self.add_buffer += text

        new_pieces = []
        offset = 0
        inserted = False  # Flag to track if the insertion is completed

        for source, start, length in self.pieces:
            if offset + length <= position:
                # Current piece is entirely before the insertion point
                new_pieces.append((source, start, length))
                offset += length
            elif not inserted:
                # Split the piece where the insertion occurs
                before_len = position - offset
                after_len = length - before_len

                if before_len > 0:
                    new_pieces.append((source, start, before_len))
                new_pieces.append(("add", add_start, len(text)))
                if after_len > 0:
                    new_pieces.append((source, start + before_len, after_len))

                inserted = True  # Mark insertion as complete
                offset += length
            else:
                # Add remaining pieces after the insertion point
                new_pieces.append((source, start, length))

        # If insertion occurs at the very end, add the new piece
        if not inserted:
            new_pieces.append(("add", add_start, len(text)))

        self.pieces = new_pieces

        print(f"After insertion, pieces: {self.pieces}")
        print(f"Current content: {self.get_content()}")

    def delete(self, position, length):
        """
        Delete text starting at a given position.
        :param position: Index where deletion starts.
        :param length: Number of characters to delete.
        """
        print(f"Deleting {length} characters at position {position}...")
        print(f"Before deletion, pieces: {self.pieces}")

        if position < 0 or position + length > self.length():
            raise ValueError("Delete range out of bounds")

        new_pieces = []
        offset = 0

        for source, start, piece_length in self.pieces:
            if offset + piece_length <= position or offset >= position + length:
                # Piece is entirely outside the deletion range
                new_pieces.append((source, start, piece_length))
            else:
                # Partial overlap with the deletion range
                before_len = max(0, position - offset)
                after_start = max(0, (position + length) - offset)

                if before_len > 0:
                    new_pieces.append((source, start, before_len))
                if after_start < piece_length:
                    new_pieces.append((source, start + after_start, piece_length - after_start))

            offset += piece_length

        self.pieces = new_pieces

        print(f"After deletion, pieces: {self.pieces}")
        print(f"Current content: {self.get_content()}")

    def length(self):
        """Return the total length of the document."""
        return sum(piece[2] for piece in self.pieces)

    def get_content(self):
        """
        Generate the full document content by combining pieces.
        :return: The full text of the document.
        """
        content = []
        for source, start, length in self.pieces:
            if source == "original":
                content.append(self.original_buffer[start:start + length])
            elif source == "add":
                content.append(self.add_buffer[start:start + length])

        result = "".join(content)
        print(f"Constructed content: {result}")
        return result
