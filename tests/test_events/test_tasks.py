import pytest
from mock.mock import AsyncMock

from app.events.tasks import send_event


@pytest.mark.asyncio
async def test_send_event(mocker):
    collect_event_data_mock = AsyncMock()
    mocker.patch("app.events.tasks.collect_event_data", collect_event_data_mock)
    collect_event_data_mock.return_value = [
        {"event_type": "message", "event_payload": "greetings"}
    ]

    send_request_mock = AsyncMock()
    mocker.patch("app.events.tasks.send_request", send_request_mock)

    await send_event()

    send_request_mock.assert_called_once_with(
        [{"event_type": "message", "event_payload": "greetings"}]
    )
