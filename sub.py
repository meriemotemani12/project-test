import redis

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

channel_name = 'test_channel'

# Subscribe to the channel
pubsub = redis_client.pubsub()
pubsub.subscribe(channel_name)

print(f"Subscribed to {channel_name}")

# Listen for messages
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received: {message['data']}")

