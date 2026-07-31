import pytest
from unittest.mock import MagicMock
import platform
import subprocess
import psutil
from local_brain import get_stats

@pytest.mark.asyncio
async def test_get_stats_darwin_with_battery(mocker):
    # Mock macOS platform
    mocker.patch('local_brain.platform.system', return_value='Darwin')

    # Mock subprocess.run for pmset
    mock_run = mocker.patch('local_brain.subprocess.run')
    mock_run.return_value.stdout = "Now drawing from 'Battery Power'\n -InternalBattery-0 (id=4653155)        85%; discharging; 2:10 remaining present: true"

    # Mock psutil
    mocker.patch('local_brain.psutil.cpu_percent', return_value=15)
    mock_vm = mocker.patch('local_brain.psutil.virtual_memory')
    mock_vm.return_value.percent = 45

    stats = await get_stats()

    assert stats['cpu'] == 15
    assert stats['ram'] == 45
    assert stats['battery'] == 85

@pytest.mark.asyncio
async def test_get_stats_darwin_no_battery(mocker):
    # Mock macOS platform
    mocker.patch('local_brain.platform.system', return_value='Darwin')

    # Mock subprocess.run for pmset
    mock_run = mocker.patch('local_brain.subprocess.run')
    mock_run.return_value.stdout = "Now drawing from 'AC Power'\n -AC Power\t(id=1)"

    # Mock psutil
    mocker.patch('local_brain.psutil.cpu_percent', return_value=20)
    mock_vm = mocker.patch('local_brain.psutil.virtual_memory')
    mock_vm.return_value.percent = 50

    stats = await get_stats()

    assert stats['cpu'] == 20
    assert stats['ram'] == 50
    assert stats['battery'] == 100

@pytest.mark.asyncio
async def test_get_stats_non_darwin_with_battery(mocker):
    # Mock Linux platform
    mocker.patch('local_brain.platform.system', return_value='Linux')

    # Mock psutil sensors_battery
    mock_batt = mocker.patch('local_brain.psutil.sensors_battery')
    mock_batt_obj = MagicMock()
    mock_batt_obj.percent = 75
    mock_batt.return_value = mock_batt_obj

    # Mock psutil
    mocker.patch('local_brain.psutil.cpu_percent', return_value=25)
    mock_vm = mocker.patch('local_brain.psutil.virtual_memory')
    mock_vm.return_value.percent = 55

    stats = await get_stats()

    assert stats['cpu'] == 25
    assert stats['ram'] == 55
    assert stats['battery'] == 75

@pytest.mark.asyncio
async def test_get_stats_non_darwin_no_battery(mocker):
    # Mock Linux platform
    mocker.patch('local_brain.platform.system', return_value='Linux')

    # Mock psutil sensors_battery returning None
    mock_batt = mocker.patch('local_brain.psutil.sensors_battery', return_value=None)

    # Mock psutil
    mocker.patch('local_brain.psutil.cpu_percent', return_value=30)
    mock_vm = mocker.patch('local_brain.psutil.virtual_memory')
    mock_vm.return_value.percent = 60

    stats = await get_stats()

    assert stats['cpu'] == 30
    assert stats['ram'] == 60
    assert stats['battery'] == 100

@pytest.mark.asyncio
async def test_get_stats_exception_fallback(mocker):
    # Mock platform to raise exception to trigger the bare except block
    mocker.patch('local_brain.platform.system', side_effect=Exception("Test Exception"))

    # Mock psutil
    mocker.patch('local_brain.psutil.cpu_percent', return_value=35)
    mock_vm = mocker.patch('local_brain.psutil.virtual_memory')
    mock_vm.return_value.percent = 65

    stats = await get_stats()

    assert stats['cpu'] == 35
    assert stats['ram'] == 65
    assert stats['battery'] == 100
