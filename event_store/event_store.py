import redis
from configs import REDIS_HOST, REDIS_PORT
import json


class EventStore:
    def __init__(self):
        self.event_store_db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def publish_event(self, key: str, event):
        serialized_event = json.dumps(event)
        self.event_store_db.set(key, serialized_event)

    def subscribe_event(self, key):
        serialized_event = self.event_store_db.get(key)
        if not serialized_event:
            return None
        deserialized_event = json.loads(serialized_event)
        return deserialized_event
