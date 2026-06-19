import pytest
from movie_song_downloader.core.event_bus import EventBus, Event


@pytest.mark.asyncio
async def test_event_bus_pub_sub():
    bus = EventBus()
    received_data = []

    async def callback(event: Event):
        received_data.append(event.data)

    # Subscribe callback to event
    await bus.subscribe("test.event", callback)

    # Publish event
    await bus.publish(Event("test.event", {"val": 42}))

    assert len(received_data) == 1
    assert received_data[0]["val"] == 42

    # Unsubscribe
    await bus.unsubscribe("test.event", callback)
    await bus.publish(Event("test.event", {"val": 100}))

    # Received list should not change
    assert len(received_data) == 1
