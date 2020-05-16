import re

import pytest

from scrapli.driver.core.cisco_iosxe.driver import PRIVS


@pytest.mark.parametrize(
    "priv_pattern",
    [("configuration", "csr1000v(config)#"), ("configuration", "csr1000v(conf-ssh-pubkey-data)#")],
    ids=["base_prompt", "ssh_key_prompt"],
)
def test_prompt_patterns(priv_pattern):
    priv_level_name = priv_pattern[0]
    prompt = priv_pattern[1]
    prompt_pattern = PRIVS.get(priv_level_name).pattern
    match = re.search(pattern=prompt_pattern, string=prompt)
    assert match


def test_on_open_on_close(mocked_iosxe_driver):
    channel_input_1 = "\n"
    channel_output_1 = "\n3560CX#"
    channel_input_2 = "terminal length 0"
    channel_output_2 = "\n3560CX#"
    channel_input_3 = "terminal width 512"
    channel_output_3 = "\n3560CX#"
    channel_input_4 = "\n"
    channel_output_4 = "\n3560CX#"
    channel_input_5 = "exit"
    channel_output_5 = ""
    test_operations = [
        (channel_input_1, channel_output_1),
        (channel_input_2, channel_output_2),
        (channel_input_3, channel_output_3),
        (channel_input_4, channel_output_4),
        (channel_input_5, channel_output_5),
    ]
    # mocked iosxe driver already calls `.open()` so we are just testing that the open commands
    # for both of these methods get sent/read back from the channel... this is mostly to ensure
    # that any change to the open/close methods are noticed and also for vanity coverage :)
    conn = mocked_iosxe_driver(test_operations)
    conn.close()
