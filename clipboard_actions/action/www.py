import re
import shlex
import subprocess
from typing import Optional

from . import Action


class Browse(Action):
    def apply(self) -> Optional[str]:
        subprocess.Popen(
            shlex.split(self.config["www"]["browser"]) + [self.clipboard()],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return None

    def enabled(self) -> bool:
        try:
            return all(
                [
                    self.config["www"]["browser"],
                    re.match(r"https?://", self.clipboard()),
                ]
            )
        except KeyError:
            return False


class OldReddit(Action):
    def apply(self) -> Optional[str]:
        return re.sub(
            r"^(https?://)(?:www\.)?(reddit\.com/)",
            r"\1old.\2",
            self.clipboard(),
        )

    def enabled(self) -> bool:
        return bool(re.match(r"https?://(?:www\.)?reddit\.com/", self.clipboard()))


class Nitter(Action):
    def apply(self) -> Optional[str]:
        return re.sub(
            r"(?:mobile\.)?twitter.com",
            self.config["www"]["nitter_url"],
            self.clipboard(),
        )

    def enabled(self) -> bool:
        try:
            return all(
                [
                    self.config["www"]["nitter_url"],
                    "twitter.com" in self.clipboard(),
                ]
            )
        except KeyError:
            return False
