import subprocess
from typing import Optional, Union


def get_clipboard(
    selection: str = "clipboard",
    target: Optional[str] = None,
    universal_newlines: bool = True,
    **kwargs
) -> str:
    xclip = subprocess.Popen(
        [
            "xclip",
            "-selection",
            selection,
            *(["-t", target] if target else []),
            "-o",
        ],
        stdout=subprocess.PIPE,
        universal_newlines=universal_newlines,
        **kwargs,
    )
    return xclip.communicate(timeout=3)[0]


def set_clipboard(
    input: Optional[Union[str, bytes]] = None,
    stdin=subprocess.PIPE,
    selection: str = "clipboard",
    target: Optional[str] = None,
    universal_newlines: bool = True,
    **kwargs
) -> None:
    xclip = subprocess.Popen(
        [
            "xclip",
            "-selection",
            selection,
            *(["-t", target] if target else []),
            "-i",
        ],
        stdin=stdin,
        universal_newlines=universal_newlines,
        **kwargs,
    )
    xclip.communicate(input, timeout=3)


def notify(title: str, body: Optional[str] = None) -> None:
    subprocess.check_call(["notify-send", title, *([body] if body else [])])
