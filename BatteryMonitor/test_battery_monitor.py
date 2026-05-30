import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add current dir to path to import battery_monitor
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import battery_monitor
from PIL import Image

class TestBatteryMonitor(unittest.TestCase):

    def test_get_system_theme_default(self):
        """Test theme defaults to dark if registry fails"""
        with patch('winreg.OpenKey', side_effect=Exception("Mock Registry Error")):
            theme = battery_monitor.get_system_theme()
            self.assertEqual(theme, "dark")

    def test_get_system_theme_light(self):
        """Test registry returns light theme"""
        with patch('winreg.OpenKey', return_value=MagicMock()), \
             patch('winreg.QueryValueEx', return_value=(1, 4)), \
             patch('winreg.CloseKey'):
            theme = battery_monitor.get_system_theme()
            self.assertEqual(theme, "light")

    def test_create_battery_icon_full(self):
        """Test drawing battery icon at 100%"""
        img = battery_monitor.create_battery_icon(100, plugged=True, low=False, theme="dark")
        self.assertIsInstance(img, Image.Image)
        self.assertEqual(img.size, (64, 64))

    def test_create_battery_icon_low(self):
        """Test drawing low battery icon"""
        img = battery_monitor.create_battery_icon(15, plugged=False, low=True, theme="light")
        self.assertIsInstance(img, Image.Image)
        self.assertEqual(img.size, (64, 64))
        
    def test_battery_info_mocked(self):
        """Test battery info extraction"""
        app = battery_monitor.BatteryMonitorApp()
        
        mock_bat = MagicMock()
        mock_bat.percent = 85.5
        mock_bat.power_plugged = True
        
        with patch('psutil.sensors_battery', return_value=mock_bat):
            percent, plugged, has_battery = app._get_battery_info()
            self.assertEqual(percent, 85)
            self.assertTrue(plugged)
            self.assertTrue(has_battery)

    def test_battery_info_no_battery(self):
        """Test fallback when no battery is found"""
        app = battery_monitor.BatteryMonitorApp()
        
        with patch('psutil.sensors_battery', return_value=None):
            percent, plugged, has_battery = app._get_battery_info()
            self.assertEqual(percent, 100)
            self.assertTrue(plugged)
            self.assertFalse(has_battery)

if __name__ == '__main__':
    unittest.main()
