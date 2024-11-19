# test_app.py
from github.AutomationDevOps.DevOpsProject.delfinen_automation_devops.app.streamlit_app import layout
from get_weather import WeatherData
import unittest
from unittest.mock import patch, MagicMock

class TestStreamlitApp(unittest.TestCase):

    @patch.object(WeatherData, 'get_current_temp')
    @patch.object(WeatherData, 'get_temp_next_24h')
    def test_layout(self, mock_get_temp_next_24h, mock_get_current_temp):
        # Mock the return values of the WeatherData methods
        mock_get_current_temp.return_value = 15.5
        mock_get_temp_next_24h.return_value = [(i, 10 + i) for i in range(24)]

        # Call the layout function
        layout()

        # Assert that the mocked methods were called
        mock_get_current_temp.assert_called_once()
        mock_get_temp_next_24h.assert_called_once()

if __name__ == '__main__':
    unittest.main()