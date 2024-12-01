class OperationalTransform:
    def __init__(self):
        self.operations = []  # Log of operations (must store dictionaries)

    def transform(self, new_op, existing_op):
        """
        Transform a new operation against an existing operation.
        :param new_op: The new operation (insert or delete).
        :param existing_op: An already-applied operation (must be a dictionary).
        :return: Transformed operation.
        """
        if not isinstance(new_op, dict) or not isinstance(existing_op, dict):
            raise TypeError("Operations must be dictionaries")

        # Insert vs Insert
        if new_op["type"] == "insert" and existing_op["type"] == "insert":
            if new_op["position"] <= existing_op["position"]:
                return new_op
            else:
                new_op["position"] += len(existing_op["text"])

        # Insert vs Delete
        elif new_op["type"] == "insert" and existing_op["type"] == "delete":
            if new_op["position"] <= existing_op["position"]:
                return new_op
            elif new_op["position"] < existing_op["position"] + existing_op["length"]:
                raise ValueError("Insert inside delete conflict")
            else:
                new_op["position"] -= existing_op["length"]

        # Delete vs Insert
        elif new_op["type"] == "delete" and existing_op["type"] == "insert":
            if new_op["position"] >= existing_op["position"]:
                new_op["position"] += len(existing_op["text"])
            elif new_op["position"] + new_op["length"] >= existing_op["position"]:
                new_op["length"] -= len(existing_op["text"])

        # Delete vs Delete
        elif new_op["type"] == "delete" and existing_op["type"] == "delete":
            if new_op["position"] >= existing_op["position"]:
                new_op["position"] -= existing_op["length"]
            elif new_op["position"] + new_op["length"] > existing_op["position"]:
                overlap = (new_op["position"] + new_op["length"]) - existing_op["position"]
                new_op["length"] -= overlap

        return new_op

    def apply(self, piece_table, op):
        """
        Apply an operation to the Piece Table.
        :param piece_table: The Piece Table instance.
        :param op: The operation (insert or delete).
        """
        if not isinstance(op, dict):
            raise TypeError("Operation must be a dictionary")
        if op["type"] == "insert":
            piece_table.insert(op["position"], op["text"])
        elif op["type"] == "delete":
            piece_table.delete(op["position"], op["length"])

        self.operations.append(op)  # Ensure only dictionaries are added
