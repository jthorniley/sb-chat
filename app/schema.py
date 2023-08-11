import hashlib
import strawberry
from strawberry.types import Info
import logging

LOGGER = logging.getLogger(__name__)


@strawberry.type
class Query:
    @strawberry.field
    def placeholder(self) -> str:
        return "hello"


@strawberry.type
class Message:
    room_name: str
    message_content: str


@strawberry.input
class SendMessageInput:
    room_name: str
    message_content: str


@strawberry.type
class Mutation:
    @strawberry.field
    async def send_message(self, info: Info, input: SendMessageInput) -> Message:
        ws = info.context["request"].consumer
        channel_layer = ws.channel_layer

        room_name_hash = hashlib.sha256(input.room_name.encode()).hexdigest()

        channel_layer_group_id = f"chat_{room_name_hash}"
        channel_layer_message = {
            "type": "chat.message",
            "room_id": f"chat_{room_name_hash}",
            "message": input.message_content,
        }

        LOGGER.info(
            "Sending channel layer message. group ID: %s, message: %s",
            channel_layer_group_id,
            channel_layer_message,
        )

        await channel_layer.group_send(
            channel_layer_group_id,
            channel_layer_message,
        )

        return Message(room_name=input.room_name, message_content=input.message_content)


schema = strawberry.Schema(query=Query, mutation=Mutation)
