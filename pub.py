import redis
import time
import random
import json

redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

while True:
    data = {"numbers": [random.randint(1, 100) for _ in range(10)]}
    redis_client.publish('data_channel', json.dumps(data))
    print(f"Published: {data}")
    time.sleep(30)