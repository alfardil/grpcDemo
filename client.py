import grpc

import todo_pb2
import todo_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = todo_pb2_grpc.TodoServiceStub(channel)

        print("adding items")
        todo_pb2.TodoItem()
        stub.AddItem(todo_pb2.TodoItem(text="code", completed=False))
        print("added ")
        stub.AddItem(todo_pb2.TodoItem(text="kill tahmid", completed=True))

        print("listing items: ")
        response_iterator = stub.ListItems(todo_pb2.Empty())

        for item in response_iterator:
            status = "[x]" if item.completed else "[ ]"
            print(f"{status} {item.text}")


if __name__ == "__main__":
    run()
