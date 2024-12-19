import redis
import time

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

channel_name = 'test_channel'

while True:
    # Publish a random number to the channel
    message = f"Random number: {time.time()}"
    redis_client.publish(channel_name, message)
    print(f"Published: {message}")
    time.sleep(5)  # Wait for 5 seconds before publishing again
