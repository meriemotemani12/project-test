import redis
import grpc
import json
from time import sleep
from concurrent import futures
import preprocessing_pb2
import preprocessing_pb2_grpc

redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

class DataStreamer(preprocessing_pb2_grpc.DataStreamerServicer):
    def StreamData(self, request_iterator, context):
        for data in request_iterator:
            numbers = data.numbers
            result = {
                "sum": sum(numbers),
                "diff": numbers[0] - numbers[1] if len(numbers) >= 2 else 0,
                "mult": numbers[0] * numbers[1] if len(numbers) >= 2 else 0,
            }
            yield preprocessing_pb2.Result(
                id=data.id,
                sum=result["sum"],
                diff=result["diff"],
                mult=result["mult"],
            )

def run_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    preprocessing_pb2_grpc.add_DataStreamerServicer_to_server(DataStreamer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server running on port 50051")
    server.start()
    server.wait_for_termination()

def redis_subscriber():
    pubsub = redis_client.pubsub()
    pubsub.subscribe('data_channel')
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            print(f"Received data: {data}")

if __name__ == '__main__':
    # Simultaneously run Redis subscription and gRPC server
    from multiprocessing import Process

    p1 = Process(target=redis_subscriber)
    p2 = Process(target=run_grpc_server)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
