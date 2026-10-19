"""
WMI temperature reader — fallback when LibreHardwareMonitor is unavailable.

Reads from MSAcpi_ThermalZoneTemperature or OpenHardwareMonitor WMI namespace.

Usage:
    from wmi_reader import read_temperatures, is_available
    temps = read_temperatures()
    # {"Thermal Zone 0": 45.0}
"""


def read_temperatures() -> dict[str, float]:
    """Read temperatures via WMI. Returns empty dict on failure."""
    temps = {}

    # Try MSAcpi_ThermalZoneTemperature (built into Windows)
    temps = _read_acpi()
    if temps:
        return temps

    # Try OpenHardwareMonitor WMI namespace
    temps = _read_ohm_wmi()
    return temps


def _read_acpi() -> dict[str, float]:
    """Read from MSAcpi_ThermalZoneTemperature."""
    temps = {}
    try:
        import wmi
        w = wmi.WMI(namespace="root\\WMI")
        sensors = w.MSAcpi_ThermalZoneTemperature()
        for i, sensor in enumerate(sensors):
            # WMI returns temperature in tenths of Kelvin
            kelvin_tenths = sensor.CurrentTemperature
            celsius = (kelvin_tenths / 10.0) - 273.15
            if 0 < celsius < 120:  # Sanity check
                temps[f"Thermal Zone {i}"] = round(celsius, 1)
    except Exception:
        pass
    return temps


def _read_ohm_wmi() -> dict[str, float]:
    """Read from OpenHardwareMonitor WMI namespace (if OHM is running)."""
    temps = {}
    try:
        import wmi
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        sensors = w.Sensor()
        for sensor in sensors:
            if sensor.SensorType == "Temperature" and sensor.Value is not None:
                name = f"{sensor.Parent} {sensor.Name}"
                # Truncate long names
                if len(name) > 30:
                    name = name[:27] + "..."
                temps[name] = float(sensor.Value)
    except Exception:
        pass
    return temps


def is_available() -> bool:
    """Check if WMI temperature reading works."""
    try:
        import wmi
        temps = _read_acpi()
        return len(temps) > 0
    except ImportError:
        return False
