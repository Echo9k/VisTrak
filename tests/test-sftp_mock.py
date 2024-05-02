import pytest
import json
import os
from unittest.mock import patch, mock_open

# Assuming the function load_configuration is in sftp-mock.py as provided
from sftp_mock import load_configuration

# Helper function to create a mock configuration file
def create_mock_config_file(config_path, config_content, config_srv_content):
    """
    Creates a mock for the configparser file and the json file it points to.
    """
    m = mock_open(read_data=config_content)
    m().readlines.return_value = config_content.splitlines()
    mock_json_open = mock_open(read_data=json.dumps(config_srv_content))

    patcher = patch("builtins.open", m)
    patcher.start()
    patcher_json = patch("builtins.open", mock_json_open, create=True)
    patcher_json.start()

    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        f.write(config_content)

    return patcher, patcher_json

@pytest.mark.parametrize("test_id, config_content, config_srv_content, expected", [
    # Happy path tests
    ("happy_path_1", "[path]\nconfig.sv=./config/srv_config.json\nsource=./data/source", {"setting": "value"}, ({"setting": "value"}, "./data/source")),
    ("happy_path_2", "[path]\nconfig.sv=./config/another_config.json\nsource=./data/another_source", {"another_setting": "another_value"}, ({"another_setting": "another_value"}, "./data/another_source")),

    # Edge cases
    # Assuming an empty json file is a valid edge case
    ("edge_case_empty_json", "[path]\nconfig.sv=./config/empty_config.json\nsource=./data/source", {}, ({}, "./data/source")),

    # Error cases
    # Assuming missing config.sv path in config file is an error case
    ("error_case_missing_config_sv", "[path]\nsource=./data/source", {"setting": "value"}, FileNotFoundError),
    # Assuming missing source path in config file is an error case
    ("error_case_missing_source", "[path]\nconfig.sv=./config/srv_config.json", {"setting": "value"}, KeyError),
])
def test_load_configuration(test_id, config_content, config_srv_content, expected):
    config_path = './config/config.conf'
    patcher, patcher_json = create_mock_config_file(config_path, config_content, config_srv_content)

    # Act
    if "error_case" in test_id:
        with pytest.raises(expected):
            load_configuration()
    else:
        result = load_configuration()

    # Assert
    if "happy_path" in test_id or "edge_case" in test_id:
        assert result == expected

    patcher.stop()
    patcher_json.stop()
