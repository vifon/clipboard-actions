from configparser import ConfigParser

from typing import Optional, Callable


class Action:
    def __init__(
        self, clipboard: Callable[..., str], config: ConfigParser
    ):
        self.clipboard = clipboard
        self.config = config

    def apply(self) -> Optional[str]:
        raise NotImplementedError()

    def enabled(self) -> bool:
        return True
