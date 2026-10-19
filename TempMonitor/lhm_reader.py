"""
LibreHardwareMonitor reader — reads CPU/GPU/SSD temps via pythonnet.

Loads LibreHardwareMonitorLib.dll and reads hardware sensors.
Returns a dict of {sensor_name: temperature_celsius}.

Usage:
    from lhm_reader import read_temperatures
    temps = read_temperatures()
    # {"CPU Package": 52.0, "GPU Core": 45.0, "SSD": 38.0}
"""

import os


def _find_dll() -> str | None:
    """Find LibreHardwareMonitorLib.dll in common locations."""
    candidates = [
        # Same directory as this script
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "LibreHardwareMonitorLib.dll"),
        # Common install locations
        r"C:\Program Files\LibreHardwareMonitor\LibreHardwareMonitorLib.dll",
        r"C:\Program Files (x86)\LibreHardwareMonitor\LibreHardwareMonitorLib.dll",
        # User's Downloads (common for portable installs)
        os.path.expanduser(r"~\Downloads\LibreHardwareMonitor\LibreHardwareMonitorLib.dll"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def read_temperatures() -> dict[str, float]:
    """
    Read temperatures from LibreHardwareMonitor.

    Returns empty dict if DLL is not found or pythonnet is not installed.
    """
    temps = {}

    try:
        import clr  # pythonnet

        dll_path = _find_dll()
        if not dll_path:
            return temps

        clr.AddReference(dll_path)
        from LibreHardwareMonitor.Hardware import Computer, SensorType

        computer = Computer()
        computer.IsCpuEnabled = True
        computer.IsGpuEnabled = True
        computer.IsStorageEnabled = True
        computer.IsMotherboardEnabled = True
        computer.Open()

        for hardware in computer.Hardware:
            hardware.Update()
            for sensor in hardware.Sensors:
                if sensor.SensorType == SensorType.Temperature and sensor.Value is not None:
                    # Shorten sensor names for readability
                    name = _shorten_name(hardware.Name, sensor.Name)
                    temps[name] = float(sensor.Value)

            # Check sub-hardware (some boards have sub-components)
            for sub in hardware.SubHardware:
                sub.Update()
                for sensor in sub.Sensors:
                    if sensor.SensorType == SensorType.Temperature and sensor.Value is not None:
                        name = _shorten_name(sub.Name, sensor.Name)
                        temps[name] = float(sensor.Value)

        computer.Close()

    except ImportError:
        pass
    except Exception:
        pass

    return temps


def _shorten_name(hw_name: str, sensor_name: str) -> str:
    """Create a short, readable sensor name."""
    # Common patterns: "Intel Core i7-12700H" → "CPU"
    hw_lower = hw_name.lower()

    if "cpu" in hw_lower or "intel" in hw_lower or "amd" in hw_lower:
        prefix = "CPU"
    elif "gpu" in hw_lower or "nvidia" in hw_lower or "radeon" in hw_lower:
        prefix = "GPU"
    elif "ssd" in hw_lower or "nvme" in hw_lower or "disk" in hw_lower:
        prefix = "SSD"
    elif "motherboard" in hw_lower or "board" in hw_lower:
        prefix = "MB"
    else:
        prefix = hw_name[:8]

    return f"{prefix} {sensor_name}"


def is_available() -> bool:
    """Check if LibreHardwareMonitor is usable."""
    try:
        import clr
        return _find_dll() is not None
    except ImportError:
        return False
