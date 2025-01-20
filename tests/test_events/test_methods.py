import pytest
from mock.mock import Mock, patch, mock_open

from app.events.methods import collect_event_data, send_request


@pytest.mark.asyncio
async def test_collect_event_data(mocker):
    config_mock = Mock()
    mocker.patch("app.events.methods.CONFIG", config_mock)
    config_mock.EVENT_JSON_PATH = "event_jsons/events.json"
    read_data = '[{"event_type": "message", "event_payload": "greetings"}]'
    with patch("builtins.open", mock_open(read_data=read_data)) as mock_file:

        actual_value = await collect_event_data()
        expected_value = [{"event_type": "message", "event_payload": "greetings"}]

        assert actual_value == expected_value
        mock_file.assert_called_with(config_mock.EVENT_JSON_PATH, "r")


@pytest.mark.asyncio
async def test_send_request(mocker):
    config_mock = Mock()
    mocker.patch("app.events.methods.CONFIG", config_mock)
    config_mock.EVENT_CONSUMER_URL = "http://127.0.0.1"
    config_mock.EVENT_CONSUMER_PORT = 5005

    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = {"message": "success"}

    requests_mock = Mock()
    mocker.patch("app.events.methods.requests", requests_mock)
    requests_mock.post.return_value = response_mock

    await send_request([{"event_type": "message", "event_payload": "greetings"}])

    requests_mock.post.assert_called_once_with(
        "http://127.0.0.1:5005/event",
        json=[{"event_type": "message", "event_payload": "greetings"}],
    )
