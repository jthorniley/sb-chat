from django.views.generic.base import TemplateView

class RoomView(TemplateView):
    template_name = "app/room.html"
