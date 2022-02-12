from configparser import ConfigParser
from functools import lru_cache
import logging
import os
import subprocess

from . import utils
from .action.action import Action

from typing import Optional, Dict, List, Type

logger = logging.getLogger(__name__)


class ActionManager:
    def __init__(self):
        self.actions: Dict[str, Action] = dict()

        config_path = os.path.join(
            os.environ.get(
                "XDG_CONFIG_HOME",
                os.path.join(os.environ["HOME"], ".config"),
            ),
            "clipboard-actions",
            "clipboard-actions.ini",
        )
        self.config = ConfigParser()
        self.config.read(config_path)

    def register(self, name: str, action: Type[Action]):
        self.actions[name] = action(self.clipboard, self.config)
        return action

    def list(self, clipboard: str) -> List[str]:
        return [
            name
            for name, action in self.actions.items()
            if action.enabled()
        ]

    def apply(self, action_name: str) -> Optional[str]:
        action = self.actions[action_name]
        try:
            return action.apply()
        except Exception:
            utils.notify("Clipboard action failed")
            logger.exception(
                'Clipboard action %s failed for clipboard "%s"',
                action,
                self.clipboard(),
            )
            return None

    @lru_cache()
    def clipboard(self, **kwargs) -> str:
        logger.debug(
            "Requesting clipboard for target: %r",
            kwargs.get("target", None),
        )
        if kwargs:
            return utils.get_clipboard(**kwargs)
        else:
            # By default use xsel(1) instead of xclip(1) as it handles
            # better the cases when no text data is available and yet
            # it's requested.
            try:
                return subprocess.check_output(
                    ["xsel", "-b", "-o"],
                    universal_newlines=True,
                    timeout=3,
                )
            except Exception:
                logger.exception("xsel has failed")
                return ""
