from flask import Flask, request, jsonify
from flask_cors import CORS
import grpc
from concurrent import futures
import prediction_pb2
import prediction_pb2_grpc
from chat import get_response
import threading

app = Flask(__name__)
CORS(app)

class PredictionServicer(prediction_pb2_grpc.PredictionServiceServicer):
    def Predict(self, request, context):
        message = request.message
        response = get_response(message)
        return prediction_pb2.PredictResponse(answer=response)

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    prediction_pb2_grpc.add_PredictionServiceServicer_to_server(PredictionServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    # Start gRPC server in a separate thread
    grpc_thread = threading.Thread(target=serve_grpc, daemon=True)
    grpc_thread.start()

    # Start Flask app
    app.run(debug=True)