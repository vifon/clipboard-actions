import shlex
import subprocess

from . import Action
import clipboard_actions.utils as utils

from typing import Optional


class Torrent(Action):
    def apply(self) -> Optional[str]:
        subprocess.check_call(
            shlex.split(self.config["torrent"]["download_program"])
            + [self.clipboard()],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        utils.notify("Torrent added")
        return None

    def enabled(self) -> bool:
        try:
            return all(
                [
                    self.config["torrent"]["download_program"],
                    self.clipboard().startswith("magnet:"),
                ]
            )
        except KeyError:
            return False
