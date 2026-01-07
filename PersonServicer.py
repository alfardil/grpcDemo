import grpc
import helloworld_pb2  # You must import the generated message definitions


class PersonServicer(object):
    """The person servicer definition."""

    def SayHi(self, request, context):
        """Says Hi"""
        # 1. Logic: gRPC methods MUST return the response message object
        return helloworld_pb2.HelloReply(message="Hi!")


def add_PersonServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "SayHi": grpc.unary_unary_rpc_method_handler(
            servicer.SayHi,
            request_deserializer=helloworld_pb2.HelloRequest.FromString,
            response_serializer=helloworld_pb2.HelloReply.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "helloworld.Greeter", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


class GreeterStub(object):
    """The client stub definition."""

    def __init__(self, channel):
        """Constructor."""
        self.SayHi = channel.unary_unary(
            "/helloworld.Greeter/SayHi",
            request_serializer=helloworld_pb2.HelloRequest.SerializeToString,
            response_deserializer=helloworld_pb2.HelloReply.FromString,
        )
