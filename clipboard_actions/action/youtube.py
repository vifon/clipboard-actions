import re
import shlex
import subprocess
from typing import Optional

import clipboard_actions.utils as utils

from . import Action


class Youtube(Action):
    def enabled(self) -> bool:
        return bool(
            re.search(
                r"^https?://(?:www\.)?youtube.com/|^https?://youtu.be/",
                self.clipboard(),
            )
        )


class Invidious(Youtube):
    def enabled(self) -> bool:
        try:
            return all(
                [
                    self.config["youtube"]["invidious_url"],
                    super().enabled(),
                ]
            )
        except KeyError:
            return False

    def apply(self) -> Optional[str]:
        return re.sub(
            r"^https?://(?:www\.)?youtube.com/|^https?://youtu.be/",
            self.config["youtube"]["invidious_url"],
            self.clipboard(),
        )


class WatchYoutube(Youtube):
    def apply(self) -> Optional[str]:
        mpv = subprocess.Popen(
            ["mpv", "--", self.clipboard()],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        utils.notify("mpv started…")
        if mpv.wait() != 0:
            utils.notify("mpv youtube", "Error")
        return None


class ListenYoutube(Youtube):
    def enabled(self) -> bool:
        try:
            return all(
                [
                    self.config["youtube"]["listen_program"],
                    super().enabled(),
                ]
            )
        except KeyError:
            return False

    def apply(self) -> Optional[str]:
        subprocess.Popen(
            shlex.split(self.config["youtube"]["listen_program"]) + [self.clipboard()],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return None
