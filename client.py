import grpc
import threading

import chat_pb2
import chat_pb2_grpc
import time


def listen_for_messages(stub):
    """
    Runs in a separate thread. Listens to the server's stream
    and prints messages as they arrive.
    """
    try:
        for note in stub.ChatStream(chat_pb2.Empty()):
            print(f"\r[{note.name}] {note.message}\n> ", end="")
    except grpc.RpcError as e:
        print(f"Disconnected: {e}")


def run():
    username = input("Enter your username: ")

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        threading.Thread(target=listen_for_messages, args=(stub,), daemon=True).start()

        print("Chat joined! Type a message and press Enter.")
        print("> ", end="")

        # send msgs
        while True:
            try:
                msg = input()
                if msg:
                    timestamp = time.time()
                    n = chat_pb2.Note(name=username, message=msg, timestamp=timestamp)
                    stub.SendNote(n)
            except EOFError:
                break


if __name__ == "__main__":
    run()
