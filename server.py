from concurrent import futures

import grpc

import todo_pb2_grpc


class TodoService(todo_pb2_grpc.TodoServiceServicer):
    def __init__(self):
        self.todos = []

    def AddItem(self, request, context):
        print(f"Adding task: {request.text}")
        self.todos.append(request)
        return request

    def ListItems(self, request, context):
        for item in self.todos:
            yield item


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoService(), server)
    server.add_insecure_port("[::]:50051")
    print("Todo Server started on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
