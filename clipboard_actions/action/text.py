import textwrap
from typing import Optional

from . import Action


class MinimizeWhitespaceLinewise(Action):
    def apply(self) -> Optional[str]:
        return "\n".join(map(str.strip, self.clipboard().split("\n"))).lstrip()

    def enabled(self) -> bool:
        return bool(self.clipboard())


class MinimizeWhitespace(Action):
    def apply(self) -> Optional[str]:
        return " ".join(self.clipboard().split())

    def enabled(self) -> bool:
        return bool(self.clipboard())


class StripIndent(Action):
    def apply(self) -> Optional[str]:
        return textwrap.dedent(self.clipboard())

    def enabled(self) -> bool:
        return bool(self.clipboard())


def fullwidth_string(string):
    chars = []
    for char in list(string):
        ord_char = ord(char)
        if ord_char == 32:
            char = chr(12288)
        elif ord_char > 32 and ord_char <= 126:
            char = chr(ord_char + 65248)
        chars.append(char)
    return "".join(chars)


class Fullwidth(Action):
    def apply(self) -> Optional[str]:
        parts = self.clipboard().split("*")
        parts[1::2] = map(fullwidth_string, parts[1::2])
        return "".join(parts)

    def enabled(self) -> bool:
        clip = self.clipboard()
        return bool(clip) and 1 <= clip.count("*") <= 2
