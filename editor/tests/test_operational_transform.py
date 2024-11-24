from editor.piece_table import PieceTable
from editor.operational_transform import OperationalTransform

# Initialize PieceTable and OT
pt = PieceTable("Hello World")
ot = OperationalTransform()

# Simulate two users making edits
op1 = {"type": "insert", "position": 6, "text": "Beautiful ", "user_id": 1, "timestamp": 1}
op2 = {"type": "delete", "position": 0, "length": 5, "user_id": 2, "timestamp": 2}

# Transform and apply operations
for existing_op in ot.operations:
    op1 = ot.transform(op1, existing_op)

ot.apply(pt, op1)

for existing_op in ot.operations:
    op2 = ot.transform(op2, existing_op)

ot.apply(pt, op2)

print("Final content:", pt.get_content())
