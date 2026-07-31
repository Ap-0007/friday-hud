import pytest
from fastapi.testclient import TestClient
from local_brain import app
import platform
import psutil
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_get_stats_mac():
    with patch("local_brain.platform.system", return_value="Darwin"):
        with patch("local_brain.subprocess.run") as mock_run:
            mock_run.return_value.stdout = "InternalBattery\t85%; discharging"
            with patch("local_brain.psutil.cpu_percent", return_value=12.5):
                with patch("local_brain.psutil.virtual_memory") as mock_vm:
                    mock_vm.return_value.percent = 45.2
                    response = client.get("/system_stats.json")
                    assert response.status_code == 200
                    assert response.json() == {"cpu": 12, "ram": 45, "battery": 85}

def test_get_stats_linux():
    with patch("local_brain.platform.system", return_value="Linux"):
        with patch("local_brain.psutil.sensors_battery") as mock_batt:
            mock_batt.return_value.percent = 92
            with patch("local_brain.psutil.cpu_percent", return_value=10.0):
                with patch("local_brain.psutil.virtual_memory") as mock_vm:
                    mock_vm.return_value.percent = 50.0
                    response = client.get("/system_stats.json")
                    assert response.status_code == 200
                    assert response.json() == {"cpu": 10, "ram": 50, "battery": 92}

def test_get_stats_no_battery():
    with patch("local_brain.platform.system", return_value="Linux"):
        with patch("local_brain.psutil.sensors_battery", return_value=None):
            with patch("local_brain.psutil.cpu_percent", return_value=10.0):
                with patch("local_brain.psutil.virtual_memory") as mock_vm:
                    mock_vm.return_value.percent = 50.0
                    response = client.get("/system_stats.json")
                    assert response.status_code == 200
                    assert response.json() == {"cpu": 10, "ram": 50, "battery": 100}

def test_get_stats_exception():
    with patch("local_brain.platform.system", side_effect=Exception("Test Error")):
        with patch("local_brain.psutil.cpu_percent", return_value=10.0):
            with patch("local_brain.psutil.virtual_memory") as mock_vm:
                mock_vm.return_value.percent = 50.0
                response = client.get("/system_stats.json")
                assert response.status_code == 200
                assert response.json() == {"cpu": 10, "ram": 50, "battery": 100}
