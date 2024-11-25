from django.db import models

class Document(models.Model):
    """
    Model to represent a collaborative document.
    """
    name = models.CharField(max_length=255, unique=True, default="UntitlednUnmastered Document")  # Document name (unique)
    content = models.TextField(default="")  # The text content of the document
    last_modified = models.DateTimeField(auto_now=True)  # Auto-updated timestamp

    def __str__(self):
        return self.name
