import pytest
from httpx import AsyncClient, ASGITransport
from local_brain import app
import platform
import subprocess
import psutil

@pytest.fixture
def test_client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")

@pytest.mark.asyncio
async def test_get_stats_darwin_success(mocker, test_client):
    mocker.patch('local_brain.platform.system', return_value="Darwin")

    mock_run = mocker.patch('local_brain.subprocess.run')
    mock_run.return_value.stdout = "Now drawing from 'Battery Power'\n -InternalBattery-0 (id=4653155)  85%; discharging; (no estimate)\n"

    response = await test_client.get("/system_stats.json")

    assert response.status_code == 200
    data = response.json()
    assert data["battery"] == 85
    assert "cpu" in data
    assert "ram" in data

@pytest.mark.asyncio
async def test_get_stats_darwin_no_internal_battery(mocker, test_client):
    mocker.patch('local_brain.platform.system', return_value="Darwin")

    mock_run = mocker.patch('local_brain.subprocess.run')
    mock_run.return_value.stdout = "Currently drawing from 'AC Power'\n -AC Power-0 (id=4653155)\n"

    response = await test_client.get("/system_stats.json")

    assert response.status_code == 200
    data = response.json()
    assert data["battery"] == 100 # default
    assert "cpu" in data
    assert "ram" in data

@pytest.mark.asyncio
async def test_get_stats_non_darwin_success(mocker, test_client):
    mocker.patch('local_brain.platform.system', return_value="Linux")

    mock_battery = mocker.Mock()
    mock_battery.percent = 75
    mocker.patch('local_brain.psutil.sensors_battery', return_value=mock_battery)

    response = await test_client.get("/system_stats.json")

    assert response.status_code == 200
    data = response.json()
    assert data["battery"] == 75
    assert "cpu" in data
    assert "ram" in data

@pytest.mark.asyncio
async def test_get_stats_non_darwin_no_battery(mocker, test_client):
    mocker.patch('local_brain.platform.system', return_value="Linux")

    mocker.patch('local_brain.psutil.sensors_battery', return_value=None)

    response = await test_client.get("/system_stats.json")

    assert response.status_code == 200
    data = response.json()
    assert data["battery"] == 100 # default
    assert "cpu" in data
    assert "ram" in data

@pytest.mark.asyncio
async def test_get_stats_exception_fallback(mocker, test_client):
    mocker.patch('local_brain.platform.system', return_value="Linux")

    # Force an exception to test the blanket except
    mocker.patch('local_brain.psutil.sensors_battery', side_effect=Exception("Failed to read battery"))

    response = await test_client.get("/system_stats.json")

    assert response.status_code == 200
    data = response.json()
    assert data["battery"] == 100 # fallback in try/except
    assert "cpu" in data
    assert "ram" in data
