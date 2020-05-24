"""scrapli.channel.base_channel"""
import re
from abc import ABC
from logging import getLogger
from typing import Union

from scrapli.helper import get_prompt_pattern, normalize_lines
from scrapli.transport.async_transport import AsyncTransport
from scrapli.transport.transport import Transport

LOG = getLogger("channel")

CHANNEL_ARGS = (
    "transport",
    "comms_prompt_pattern",
    "comms_return_char",
    "comms_ansi",
    "timeout_ops",
)


class ChannelBase(ABC):
    def __init__(
        self,
        transport: Union[Transport, AsyncTransport],
        comms_prompt_pattern: str = r"^[a-z0-9.\-@()/:]{1,32}[#>$]$",
        comms_return_char: str = "\n",
        comms_ansi: bool = False,
        comms_auto_expand: bool = False,
        timeout_ops: int = 10,
    ):
        """
        Channel Object

        Args:
            transport: Transport object of any transport provider (system|telnet or a plugin)
                transport could in theory be any transport as long as it provides a read and a write
                method... obviously its probably always going to be scrapli transport though
            comms_prompt_pattern: raw string regex pattern -- use `^` and `$` for multi-line!
            comms_return_char: character to use to send returns to host
            comms_ansi: True/False strip comms_ansi characters from output
            comms_auto_expand: bool to indicate if a device auto-expands commands, for example
                juniper devices without `cli complete-on-space` disabled will convert `config` to
                `configuration` after entering a space character after `config`; because scrapli
                reads the channel until each command is entered, the command changing from `config`
                to `configuration` will cause scrapli (by default) to never think the command has
                been entered. Setting this value to `True` will force scrapli to zip the split lists
                of inputs and outputs together to determine if each read output starts with the
                corresponding input. For example, if the inputs are "sho ver" and the read output is
                "show version", scrapli will zip the split strings together and confirm that in fact
                "show" starts with "sho" and "version" starts with "ver", confirming that the
                commands that were input were input properly. This is disabled by default, as it is
                preferable to disable this type of behavior via the device itself if possible.
            timeout_ops: timeout in seconds for channel operations (reads/writes)

        Args:
            N/A

        Returns:
            N/A  # noqa: DAR202

        Raises:
            N/A

        """
        LOG.name = f"channel-{transport.host}"

        self.transport = transport
        self.comms_prompt_pattern = comms_prompt_pattern
        self.comms_return_char = comms_return_char
        self.comms_ansi = comms_ansi
        self.comms_auto_expand = comms_auto_expand
        self.timeout_ops = timeout_ops

    def __str__(self) -> str:
        """
        Magic str method for Channel

        Args:
            N/A

        Returns:
            str: str for class object

        Raises:
            N/A

        """
        return "scrapli Channel Object"

    def __repr__(self) -> str:
        """
        Magic repr method for Channel

        Args:
            N/A

        Returns:
            str: repr for class object

        Raises:
            N/A

        """
        class_dict = self.__dict__.copy()
        class_dict.pop("transport")
        return f"scrapli Channel {class_dict}"

    def _restructure_output(self, output: bytes, strip_prompt: bool = False) -> bytes:
        """
        Clean up preceding empty lines, and strip prompt if desired

        Args:
            output: bytes from channel
            strip_prompt: bool True/False whether to strip prompt or not

        Returns:
            bytes: output of joined output lines optionally with prompt removed

        Raises:
            N/A

        """
        output = normalize_lines(output=output)

        if not strip_prompt:
            return output

        # could be compiled elsewhere, but allow for users to modify the prompt whenever they want
        prompt_pattern = get_prompt_pattern(prompt="", class_prompt=self.comms_prompt_pattern)
        output = re.sub(pattern=prompt_pattern, repl=b"", string=output)
        return output

    def _send_return(self) -> None:
        """
        Send return char to device

        Args:
            N/A

        Returns:
            N/A  # noqa: DAR202

        Raises:
            N/A

        """
        self.transport.write(channel_input=self.comms_return_char)
        LOG.debug(f"Write (sending return character): {repr(self.comms_return_char)}")