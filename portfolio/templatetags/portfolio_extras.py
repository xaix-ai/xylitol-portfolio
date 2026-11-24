"""
Helpers for showing images and videos that are saved in the database as text.

In the admin you can type an image in three ways:

  1. A file name inside portfolio/static/portfolio/images/
       e.g.  projects/sales-dashboard-1.png
  2. A full link to an image on the internet
       e.g.  https://i.imgur.com/abc123.png
  3. A Google Drive share link (the file must be shared as "Anyone with the link")
       e.g.  https://drive.google.com/file/d/FILE_ID/view?usp=sharing
"""

import re

from django import template
from django.templatetags.static import static
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg")
VIDEO_EXTENSIONS = (".mp4", ".webm", ".mov", ".m4v")

_DRIVE_PATTERNS = (
    re.compile(r"drive\.google\.com/file/d/([\w-]+)"),
    re.compile(r"drive\.google\.com/(?:open|uc)\?(?:.*&)?id=([\w-]+)"),
)


def _clean(value):
    return (value or "").strip()


def _path_only(value):
    return _clean(value).lower().split("?")[0].split("#")[0]


def _drive_id(value):
    for pattern in _DRIVE_PATTERNS:
        match = pattern.search(value)
        if match:
            return match.group(1)
    return None


@register.filter
def media_src(value):
    """Turn whatever was typed in the admin into a working image/video address."""
    value = _clean(value)
    if not value:
        return ""

    drive_id = _drive_id(value)
    if drive_id:
        return f"https://lh3.googleusercontent.com/d/{drive_id}"

    if value.startswith(("http://", "https://", "/", "data:")):
        return value

    # A plain file name: look for it in portfolio/static/portfolio/images/
    value = value.removeprefix("./")
    value = value.removeprefix("portfolio/static/portfolio/images/")
    value = value.removeprefix("static/portfolio/images/")
    value = value.removeprefix("images/")
    return static("portfolio/images/" + value)


@register.filter
def media_kind(media):
    """'video' or 'image' for a ProjectMedia row (type text is forgiving)."""
    kind = _clean(getattr(media, "media_type", "")).lower()
    url = _path_only(getattr(media, "media_url", ""))
    if "video" in kind or "recording" in kind or url.endswith(VIDEO_EXTENSIONS):
        return "video"
    return "image"


@register.filter
def is_image(value):
    """True when a link points at a picture (used for certificate previews)."""
    value = _clean(value)
    if not value:
        return False
    if _drive_id(value):
        return True
    return _path_only(value).endswith(IMAGE_EXTENSIONS)


@register.filter
def pretty_url(value):
    """https://www.example.com/app/ -> example.com/app"""
    value = _clean(value)
    value = re.sub(r"^https?://", "", value)
    value = value.removeprefix("www.")
    return value.rstrip("/")


_BULLET = re.compile(r"^(?:[-*•●▪◦]|\d+[.)])\s+(.*)$")


@register.filter(needs_autoescape=True)
def rich_text(value, autoescape=True):
    """
    Lets descriptions typed in the admin keep their shape:
      - lines starting with -, *, • or "1." become a bullet list
      - an empty line starts a new paragraph
      - other line breaks are kept
    """
    escape = conditional_escape if autoescape else (lambda text: text)
    html, items, paragraph = [], [], []

    def flush_items():
        if items:
            html.append(
                '<ul class="card-bullets">'
                + "".join(f"<li>{escape(item)}</li>" for item in items)
                + "</ul>"
            )
            items.clear()

    def flush_paragraph():
        if paragraph:
            html.append("<p>" + "<br>".join(escape(line) for line in paragraph) + "</p>")
            paragraph.clear()

    for raw in (value or "").splitlines():
        line = raw.strip()
        bullet = _BULLET.match(line)
        if bullet:
            flush_paragraph()
            items.append(bullet.group(1))
        elif not line:
            flush_items()
            flush_paragraph()
        else:
            flush_items()
            paragraph.append(line)

    flush_items()
    flush_paragraph()
    return mark_safe("".join(html))
