import strawberry

@strawberry.type
class Query:
    @strawberry.field
    def placeholder(self) -> str:
        return "hello"

@strawberry.input
class SendMessageInput:
    message_content: str

@strawberry.type
class Message:
    message_content: str

@strawberry.type
class Mutation:
    @strawberry.field
    async def sendMessage(input: SendMessageInput) -> Message:
        ...


schema = strawberry.Schema(query=Query, mutation=Mutation)