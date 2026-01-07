from concurrent import futures
import grpc
import time
import chat_pb2
import chat_pb2_grpc


class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        # store messages
        self.chats: list[chat_pb2.Note] = []

    def ChatStream(self, request, context):
        """
        Stream all chat messages to the client.
        It first sends history, then waits for new messages.
        """
        last_index = 0
        while True:
            while len(self.chats) > last_index:
                n = self.chats[last_index]
                last_index += 1
                yield n

            # Wait a bit before checking again to save CPU
            time.sleep(0.1)

    def SendNote(self, request: chat_pb2.Note, context):
        """
        Receive a note from a client and add it to the history.
        """
        arrival_time = time.time()
        latency = arrival_time - request.timestamp
        print(f"[{request.name}] {request.message}| Latency: {latency}")
        self.chats.append(request)
        return chat_pb2.Empty()

    def send_broadcast(self, message):
        """Allows the server code to inject a message."""
        print(f"[SERVER BROADCAST] {message}")
        note = chat_pb2.Note(name="ADMIN", message=message)
        self.chats.append(note)


def serve():
    chat_service = ChatService()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(chat_service, server)
    server.add_insecure_port("[::]:50051")
    print("Chat Server started on port 50051...")
    server.start()
    print("Write a broadcast message below: ")
    try:
        while True:
            msg = input()
            if msg:
                chat_service.send_broadcast(msg)
    except KeyboardInterrupt:
        print("\nStopping server")
        server.stop(0)


if __name__ == "__main__":
    serve()
