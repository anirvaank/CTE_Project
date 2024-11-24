from django.urls import path
from editor.consumers import EditorConsumer

websocket_urlpatterns = [
    path('ws/editor/<int:document_id>/', EditorConsumer.as_asgi()),
]
