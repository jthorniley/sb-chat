"""
ASGI config for sb_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from strawberry.channels import GraphQLProtocolTypeRouter
 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sb_chat.settings")

django = get_asgi_application()

from app.schema import schema # noqa
 
 
application = GraphQLProtocolTypeRouter(
    schema,
    django_application=django,
)