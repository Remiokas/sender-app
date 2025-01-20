import pytest
from fastapi.testclient import TestClient
from mock.mock import Mock, MagicMock, patch
from app.main import app, create_scheduler, lifespan_handler

client = TestClient(app)


def test_healthcheck():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_scheduler(mocker):
    config_mock = Mock()
    mocker.patch("app.main.CONFIG", config_mock)
    config_mock.SEND_INTERVAL = 20

    scheduler_mock = Mock()
    mocker.patch("app.main.BackgroundScheduler", return_value=scheduler_mock)

    with patch("app.main.IntervalTrigger") as interval_mock:
        with patch("app.main.run_async_job") as run_async_job_mock:
            with patch("app.main.send_event") as send_event_mock:
                interval = interval_mock.return_value
                create_scheduler()

                scheduler_mock.add_job.assert_called_once_with(
                    run_async_job_mock, interval, args=[send_event_mock]
                )


@pytest.mark.asyncio
async def test_lifespan_handler(mocker):
    create_scheduler_mock = MagicMock()
    mocker.patch("app.main.create_scheduler", return_value=create_scheduler_mock)

    async with lifespan_handler(app):
        pass

    create_scheduler_mock.start.assert_called_once()
    create_scheduler_mock.shutdown.asser_called_once()
