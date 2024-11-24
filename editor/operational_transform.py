class OperationalTransform:
    def __init__(self):
        self.operations = []  # Log of operations

    def transform(self, new_op, existing_op):
        """
        Transform a new operation against an existing operation.
        :param new_op: The new operation (insert or delete).
        :param existing_op: An already-applied operation.
        :return: Transformed operation.
        """
        if new_op["type"] == "insert" and existing_op["type"] == "insert":
            if new_op["position"] <= existing_op["position"]:
                # No adjustment needed
                return new_op
            else:
                # Shift the new insertion to the right
                new_op["position"] += len(existing_op["text"])

        elif new_op["type"] == "insert" and existing_op["type"] == "delete":
            if new_op["position"] <= existing_op["position"]:
                # No adjustment needed
                return new_op
            elif new_op["position"] < existing_op["position"] + existing_op["length"]:
                # Split the insertion (conflict resolution)
                raise ValueError("Insert inside delete conflict")
            else:
                # Shift the new insertion left
                new_op["position"] -= existing_op["length"]

        elif new_op["type"] == "delete" and existing_op["type"] == "insert":
            if new_op["position"] >= existing_op["position"]:
                # Shift the delete right
                new_op["position"] += len(existing_op["text"])
            elif new_op["position"] + new_op["length"] >= existing_op["position"]:
                # Adjust delete length
                new_op["length"] -= len(existing_op["text"])

        elif new_op["type"] == "delete" and existing_op["type"] == "delete":
            if new_op["position"] >= existing_op["position"]:
                # Shift delete left
                new_op["position"] -= existing_op["length"]
            elif new_op["position"] + new_op["length"] > existing_op["position"]:
                # Adjust delete length
                overlap = (new_op["position"] + new_op["length"]) - existing_op["position"]
                new_op["length"] -= overlap

        return new_op

    def apply(self, piece_table, op):
        """
        Apply an operation to the PieceTable.
        :param piece_table: The PieceTable instance.
        :param op: The operation (insert or delete).
        """
        if op["type"] == "insert":
            piece_table.insert(op["position"], op["text"])
        elif op["type"] == "delete":
            piece_table.delete(op["position"], op["length"])

        # Log the operation
        self.operations.append(op)
