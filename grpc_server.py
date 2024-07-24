import grpc
import example_pb2
import example_pb2_grpc
from concurrent import futures
import logging

class YourServiceServicer(example_pb2_grpc.YourServiceServicer):
    def YourMethod(self, request, context):
        input_string = request.input
        logging.info(f"Received request with input: {input_string}")
        # Process the input
        output_string = f"Processed: {input_string}"
        return example_pb2.YourResponse(output=output_string)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_YourServiceServicer_to_server(YourServiceServicer(), server)
    port = 50051
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"Server started, listening on {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting gRPC server...")
    serve()