import asyncio
import logging
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Any

logger = logging.getLogger("movie_song_downloader.EventBus")


@dataclass
class Event:
    type: str
    data: Dict[str, Any] = field(default_factory=dict)


class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = asyncio.Lock()

    async def subscribe(self, event_type: str, callback: Callable) -> None:
        async with self._lock:
            self._subscribers.setdefault(event_type, []).append(callback)

    async def unsubscribe(self, event_type: str, callback: Callable) -> None:
        async with self._lock:
            if event_type in self._subscribers:
                try:
                    self._subscribers[event_type].remove(callback)
                except ValueError:
                    pass

    async def publish(self, event: Event) -> None:
        async with self._lock:
            callbacks = list(self._subscribers.get(event.type, []))
        for cb in callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(event)
                else:
                    cb(event)
            except Exception as e:
                logger.error(f"Callback error for {event.type}: {e}", exc_info=True)

    def publish_fire_and_forget(self, event: Event) -> None:
        callbacks = list(self._subscribers.get(event.type, []))
        for cb in callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    asyncio.create_task(cb(event))
                else:
                    cb(event)
            except Exception as e:
                logger.error(
                    f"Fire-and-forget error for {event.type}: {e}", exc_info=True
                )


event_bus = EventBus()
