from typing import Any, Dict
from django.views.generic.base import TemplateView
import re
from django.http import Http404


class RoomView(TemplateView):
    template_name = "app/room.html"

    def get_context_data(self, room_name: str, **kwargs) -> Dict[str, Any]:
        if not re.match("^[A-Za-z0-9_\- ]+$", room_name):
            # possibly unsafe / unprintable room name, no
            raise Http404
        return {
            **kwargs,
            "room_name": room_name,
        }
