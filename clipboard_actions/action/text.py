from . import Action

from typing import Optional

import textwrap


class StripLinewise(Action):
    def apply(self) -> Optional[str]:
        return "\n".join(
            map(str.strip, self.clipboard().split("\n"))
        ).lstrip()

    def enabled(self) -> bool:
        return bool(self.clipboard())


class StripAll(Action):
    def apply(self) -> Optional[str]:
        return " ".join(self.clipboard().split())

    def enabled(self) -> bool:
        return bool(self.clipboard())


class StripIndent(Action):
    def apply(self) -> Optional[str]:
        return textwrap.dedent(self.clipboard())

    def enabled(self) -> bool:
        return bool(self.clipboard())
