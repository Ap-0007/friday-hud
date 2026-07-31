import pytest
from stats_bridge import get_stats

def test_get_stats_with_battery(mocker):
    mock_battery = mocker.Mock()
    mock_battery.percent = 85
    mock_battery.power_plugged = True

    mocker.patch('psutil.sensors_battery', return_value=mock_battery)
    mocker.patch('psutil.cpu_percent', return_value=15.5)

    mock_ram = mocker.Mock()
    mock_ram.percent = 45.0
    mocker.patch('psutil.virtual_memory', return_value=mock_ram)

    mocker.patch('time.time', return_value=1620000000.0)

    stats = get_stats()

    assert stats == {
        "cpu": 15.5,
        "ram": 45.0,
        "battery": 85,
        "charging": True,
        "timestamp": 1620000000.0
    }

def test_get_stats_without_battery(mocker):
    mocker.patch('psutil.sensors_battery', return_value=None)
    mocker.patch('psutil.cpu_percent', return_value=20.0)

    mock_ram = mocker.Mock()
    mock_ram.percent = 50.0
    mocker.patch('psutil.virtual_memory', return_value=mock_ram)

    mocker.patch('time.time', return_value=1620000000.0)

    stats = get_stats()

    assert stats == {
        "cpu": 20.0,
        "ram": 50.0,
        "battery": 100,
        "charging": True,
        "timestamp": 1620000000.0
    }
