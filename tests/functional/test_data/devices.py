from pathlib import Path

import scrapli
from scrapli import Scrape
from scrapli.driver.core import EOSDriver, IOSXEDriver, IOSXRDriver, JunosDriver, NXOSDriver

TEST_DATA_PATH = f"{Path(scrapli.__file__).parents[1]}/tests/functional/test_data"

USERNAME = "vrnetlab"
PASSWORD = "VR-netlab9"
PRIVATE_KEY = f"{TEST_DATA_PATH}/vrnetlab_key"
INVALID_PRIVATE_KEY = f"{TEST_DATA_PATH}/__init__.py"

DEVICES = {
    "cisco_iosxe": {
        "driver": IOSXEDriver,
        "auth_username": USERNAME,
        "auth_password": PASSWORD,
        "auth_secondary": PASSWORD,
        "auth_strict_key": False,
        "host": "172.18.0.11",
        "base_config": f"{TEST_DATA_PATH}/base_configs/cisco_iosxe",
    },
    "cisco_nxos": {
        "driver": NXOSDriver,
        "auth_username": USERNAME,
        "auth_password": PASSWORD,
        "auth_secondary": PASSWORD,
        "auth_strict_key": False,
        "host": "172.18.0.12",
        "base_config": f"{TEST_DATA_PATH}/base_configs/cisco_nxos",
    },
    "cisco_iosxr": {
        "driver": IOSXRDriver,
        "auth_username": USERNAME,
        "auth_password": PASSWORD,
        "auth_secondary": PASSWORD,
        "auth_strict_key": False,
        "host": "172.18.0.13",
        "base_config": f"{TEST_DATA_PATH}/base_configs/cisco_iosxr",
    },
    "arista_eos": {
        "driver": EOSDriver,
        "auth_username": USERNAME,
        "auth_password": PASSWORD,
        "auth_secondary": PASSWORD,
        "auth_strict_key": False,
        "host": "172.18.0.14",
        "comms_ansi": True,
        "base_config": f"{TEST_DATA_PATH}/base_configs/arista_eos",
    },
    "juniper_junos": {
        "driver": JunosDriver,
        "auth_username": USERNAME,
        "auth_password": PASSWORD,
        "auth_secondary": PASSWORD,
        "auth_strict_key": False,
        "host": "172.18.0.15",
        "base_config": f"{TEST_DATA_PATH}/base_configs/juniper_junos",
    },
    "linux": {
        "driver": Scrape,
        "auth_username": "root",
        "auth_password": "docker",
        "auth_strict_key": False,
        "host": "172.18.0.20",
        "comms_ansi": True,
        "comms_prompt_pattern": r"^linux:~#\s*$",
    },
}
