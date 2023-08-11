import hashlib
from inspect import cleandoc
from typing import AsyncGenerator
import strawberry
from strawberry.types import Info
import logging

LOGGER = logging.getLogger(__name__)


@strawberry.type
class Query:
    @strawberry.field(
        description="Meaningless placeholder, becuase query schema can't be empty"
    )
    def placeholder(self) -> str:
        return "hello"


@strawberry.type(
    description=cleandoc(
        """
        A message delivered to a chat room

            roomName: name of the room
            messageContent: what has been said
        """
    )
)
class ChatRoomMessage:
    room_name: str
    message_content: str


@strawberry.input(
    description=cleandoc(
        """
        Arguments to sendChatRoomMessage

            roomName: name of the room to send to
            messageContent: what the user wants to say

        """
    )
)
class SendChatRoomMessageInput:
    room_name: str
    message_content: str


@strawberry.type
class Mutation:
    @strawberry.field(description="Send message to chat room")
    async def send_chat_room_message(
        self, info: Info, input: SendChatRoomMessageInput
    ) -> ChatRoomMessage:
        ws = info.context["request"].consumer
        channel_layer = ws.channel_layer

        room_name_hash = hashlib.sha256(input.room_name.encode()).hexdigest()

        channel_layer_group_id = f"chat_{room_name_hash}"
        channel_layer_message = {
            "type": "chat.message",
            "room_name": input.room_name,
            "message_content": input.message_content,
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

        return ChatRoomMessage(
            room_name=input.room_name, message_content=input.message_content
        )


@strawberry.input(
    description=cleandoc(
        """
        Arguments to chatRoomMessages subscription.

            roomName: name of the room to listen for messages in

        """
    )
)
class ChatRoomMessagesInput:
    room_name: str


@strawberry.type
class Subscription:
    @strawberry.subscription("Get messages delivered to a chat room as they arrive")
    async def chat_room_messages(
        self, info: Info, input: ChatRoomMessagesInput
    ) -> AsyncGenerator[ChatRoomMessage, None]:
        ws = info.context["request"]
        channel_layer = ws.channel_layer

        room_name_hash = hashlib.sha256(input.room_name.encode()).hexdigest()
        group_id = f"chat_{room_name_hash}"

        await channel_layer.group_add(group_id, ws.channel_name)

        LOGGER.info("subscription starting")
        async with ws.listen_to_channel(
            "chat.message", groups=[group_id]
        ) as async_listener:
            async for message in async_listener:
                if input.room_name == message["room_name"]:
                    LOGGER.info(
                        "Receiving message. Group id: %s, message: %s",
                        group_id,
                        message,
                    )
                    yield ChatRoomMessage(
                        room_name=message["room_name"],
                        message_content=message["message_content"],
                    )


schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
