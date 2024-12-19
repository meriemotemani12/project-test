import grpc
import preprocessing_pb2
import preprocessing_pb2_grpc
import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="password",
    host="db",
    port="5432"
)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id SERIAL PRIMARY KEY,
        sum INTEGER,
        diff INTEGER,
        mult INTEGER
    )
""")
conn.commit()

def run_grpc_client():
    with grpc.insecure_channel('data_preprocessor:50051') as channel:
        stub = preprocessing_pb2_grpc.DataStreamerStub(channel)
        response = stub.StreamData(preprocessing_pb2.DataRequest())
        for result in response:
            print(f"Result received: {result}")
            cursor.execute(
                "INSERT INTO results (sum, diff, mult) VALUES (%s, %s, %s)",
                (result.sum, result.diff, result.mult)
            )
            conn.commit()

if __name__ == '__main__':
    run_grpc_client()
