import mimetypes
import os
import re
import subprocess
import sys
import tempfile
from typing import List, Optional

import httpx

import clipboard_actions.utils as utils

from . import Action


class Image(Action):
    _image_target: Optional[str] = None

    @property
    def image_target(self) -> Optional[str]:
        if self._image_target is None:
            targets = self._image_targets()
            if targets:
                self._image_target = targets[0]
        return self._image_target

    def _image_targets(self) -> List[str]:
        try:
            output = self.clipboard(target="TARGETS")
            assert isinstance(output, str)
        except subprocess.CalledProcessError:
            return []
        else:
            targets = output.split("\n")

            def is_image(target: str) -> bool:
                return target.startswith("image/")

            return list(filter(is_image, targets))

    def enabled(self) -> bool:
        return bool(self.image_target)


class ImageTmpfile(Image):
    def apply(self) -> Optional[str]:
        assert isinstance(self.image_target, str)

        file_type = mimetypes.guess_extension(self.image_target)
        image_data = self.clipboard(
            target=self.image_target,
            universal_newlines=False,
        )
        assert isinstance(image_data, bytes)
        with tempfile.NamedTemporaryFile(
            prefix="image-",
            suffix=file_type,
            delete=False,
        ) as fh:
            try:
                fh.write(image_data)
            except Exception:
                os.unlink(fh.name)
                raise
            return fh.name


class ImageEdit(ImageTmpfile):
    def editor(self, path: str) -> bool:
        "Return whether to update the clipboard with a modified image."
        raise NotImplementedError()

    def edit(self, path: str) -> bool:
        "Return whether to update the clipboard with a modified image."
        old_mtime = os.path.getmtime(path)
        return_value = self.editor(path)
        new_mtime = os.path.getmtime(path)
        return return_value and old_mtime != new_mtime

    def apply(self) -> Optional[str]:
        image_path = super().apply()

        assert isinstance(image_path, str)
        assert isinstance(self.image_target, str)

        try:
            if self.edit(image_path):
                with open(image_path, "r") as fh:
                    utils.set_clipboard(
                        target=self.image_target,
                        universal_newlines=False,
                        stdin=fh,
                    )
        finally:
            os.unlink(image_path)
        return None


class ImageView(ImageEdit):
    def editor(self, path: str) -> bool:
        subprocess.check_call(["sxiv", path], stdout=sys.stderr.fileno())
        return True


class ImageEditGIMP(ImageEdit):
    def editor(self, path: str) -> bool:
        subprocess.check_call(["gimp", path], stdout=sys.stderr.fileno())
        return True


class ImageEditMTPaint(ImageEdit):
    def editor(self, path: str) -> bool:
        subprocess.check_call(["mtpaint", path], stdout=sys.stderr.fileno())
        return True


class ImageUpload(ImageEdit):
    """Upload an image from the clipboard and store an URL to it."""

    def enabled(self) -> bool:
        try:
            return all(
                [
                    self.config["image"]["upload_command"],
                    super().enabled(),
                ]
            )
        except KeyError:
            return False

    def editor(self, path: str) -> bool:
        subprocess.check_call(
            [self.config["image"]["upload_command"], path],
            stdout=sys.stderr.fileno(),
        )
        return False


class ImageLoad(Action):
    """Load an image from a path and store it in the clipboard."""

    def apply(self) -> Optional[str]:
        with open(self.clipboard(), "r") as fh:
            utils.set_clipboard(
                target=mimetypes.guess_type(fh.name)[0],
                universal_newlines=False,
                stdin=fh,
            )
        utils.notify("Image loaded")
        return None

    def enabled(self) -> bool:
        path = self.clipboard()
        if path.startswith("/"):
            mime, encoding = mimetypes.guess_type(path)
            return (
                mime is not None and mime.startswith("image/") and os.path.exists(path)
            )
        else:
            return False


class ImageFetch(Action):
    """Fetch an image from an URL and store it in the clipboard."""

    def apply(self) -> Optional[str]:
        url = self.clipboard()
        res = httpx.get(url)
        res.raise_for_status()

        try:
            compress = self.config.getboolean("image", "compress")
        except KeyError:
            compress = False

        if compress:
            content = subprocess.Popen(
                ["pngquant", "-"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
            ).communicate(res.content)[0]
        else:
            content = res.content

        utils.set_clipboard(
            target=mimetypes.guess_type(url)[0],
            universal_newlines=False,
            input=content,
        )
        utils.notify("Image fetched")
        return None

    def enabled(self) -> bool:
        url = self.clipboard()
        if re.match(r"https?://", url):
            mime, encoding = mimetypes.guess_type(url)
            return mime is not None and mime.startswith("image/")
        else:
            return False


class ImageLoadOrFetch(Action):
    def __init__(self, *args, **kwargs):
        self.local_loader = ImageLoad(*args, **kwargs)
        self.remote_fetcher = ImageFetch(*args, **kwargs)
        self.local = self.remote = False

    def apply(self) -> Optional[str]:
        if self.local:
            return self.local_loader.apply()
        elif self.remote:
            return self.remote_fetcher.apply()
        else:
            assert False

    def enabled(self) -> bool:
        self.local = self.local_loader.enabled()
        self.remote = self.remote_fetcher.enabled()
        return self.local or self.remote
