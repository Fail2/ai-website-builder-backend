import asyncio
from collections import defaultdict

class EventHub:
    def __init__(self):
        self.queues = defaultdict(asyncio.Queue)

    async def publish(self, project_id, event):
        await self.queues[str(project_id)].put(event)

    async def subscribe(self, project_id):
        return self.queues[str(project_id)]

event_hub = EventHub()