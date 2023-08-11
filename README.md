# Example chat room application using strawberry-graphql and channels

To configure use poetry + django management:

```
poetry install
poetry run python manage.py migrate
```

To run the dev server, use:

* django dev server: `poetry run python manage.py runserver`
* daphne directly: `poetry run daphne -b 0.0.0.0 -p 8000 sb_chat.asgi:application`
* (n.b. these are both for local dev, there is no production-safe configuration)

Go to a chat room by putting a "room name" into a URL, e.g. http://localhost:8000/room%201/

Send a message with the text input + press enter.

TODO: there is no UI for receiving messages, use the GraphiQL dev UI to create the subscription:

http://localhost:8000/graphql/

Query:

```
subscription chatRoomMessages ($roomName: String!) {
  chatRoomMessages(input: {roomName: $roomName}) {
    roomName
    messageContent
  }
}
```

Variables:

```
{
  "roomName": "room 1"
}
```

(or whatever `roomName` you are sending messages to)

