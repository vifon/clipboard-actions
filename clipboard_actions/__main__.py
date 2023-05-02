import logging
import subprocess

import clipboard_actions.utils as utils

from .action import *
from .action_manager import ActionManager

logging.basicConfig(level=logging.INFO)

actions = {
    "Watch YouTube": WatchYoutube,
    "Youtube to Invidious": Invidious,
    "Listen YouTube": ListenYoutube,
    "Download Torrent": Torrent,
    "View image": ImageView,
    "Edit with GIMP": ImageEditGIMP,
    "Edit with mtpaint": ImageEditMTPaint,
    "Upload image": ImageUpload,
    "Fetch image": ImageLoadOrFetch,
    "Save image to file": ImageTmpfile,
    "Twitter to Nitter": Nitter,
    "Reddit Old": OldReddit,
    "Browse": Browse,
    "Minimize whitespace": MinimizeWhitespace,
    "Minimize whitespace linewise": MinimizeWhitespaceLinewise,
    "Strip indent": StripIndent,
    "Fullwidth": Fullwidth,
}


def main():
    manager = ActionManager()
    for name, action in actions.items():
        manager.register(name, action)

    clipboard_preview = manager.clipboard().replace("\n", "⏎")
    if len(clipboard_preview) > 40:
        clipboard_preview = "{}…{}".format(
            clipboard_preview[:25], clipboard_preview[-15:]
        )

    dmenu = subprocess.Popen(
        [
            "dmenu",
            "-f",
            "-i",
            "-l",
            "16",
            "-p",
            "Clipboard: {}".format(clipboard_preview),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    actions_list = "\n".join(manager.list(manager.clipboard()))
    action = dmenu.communicate(actions_list)[0].strip()

    if dmenu.returncode == 0 and action:
        result = manager.apply(action)
        if result:
            utils.set_clipboard(input=result)


if __name__ == "__main__":
    main()
