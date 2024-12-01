from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'editor/(?P<document_id>\w+)/$', consumers.EditorConsumer.as_asgi()),
]
