# Generate Python code AND the .pyi type stubs
generate:
    python -m grpc_tools.protoc \
        -I. \
        --python_out=. \
        --grpc_python_out=. \
        --mypy_out=. \
        chat.proto

env *args:
    pipenv install --dev {{args}}
    pipenv shell

# Run server
server *args:
    python server.py {{args}}

# Run client
client *args:
    python client.py {{args}}

# Clean up all auto-generated files
clean *args:
    rm *_pb2.py *_pb2_grpc.py *_pb2.pyi {{args}}
