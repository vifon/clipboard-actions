clipboard-actions
=================

Heavily opinionated contextual clipboard actions and transformers.
Mostly cut specifically for my personal needs, but I'm sure someone
else will be able to find a use for it one way or another.

Features
--------

Actions are provided contextually according to the current contents of
the clipboard.  For example the image upload action is provided only
if the clipboard contains an image, whitespace cleanup will be
provided for any text and Youtube-specific actions will appear only
for Youtube links.

Some of the available actions:

* Whitespace cleanup
* Image upload with a custom program (not included, must be provided by the user)
* URL manipulation to redirect to replacement services (e.g. Invidious for Youtube, Nitter for Twitter)
* URL handling with specialized tools for appropriate URLs (`mpv` with
  `yt-dlp` for Youtube, `transmission-remote` for Magnet links, etc.)

A non-exhaustive graph of available actions and clipboard
transformations:

![](https://raw.githubusercontent.com/vifon/clipboard-actions/master/examples/graph.png)

Usage
-----

1. Copy `clipboard-actions.ini` to
   `~/.config/clipboard-actions/clipboard-actions.ini` and customize
   as needed.
2. Bind the `clipboard-actions` command to a key such as
   <kbd>Mod4+v</kbd>.

Known Issues
------------

* Limited support for image formats.  Anything that's not a plain PNG
  file will probably fail one way or another.
