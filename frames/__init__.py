"""All frames to be rendered on each corner of the window."""

from typing import Literal, Optional


def generate_font(
        font_face: str = 'Helvetica', font_size: int = 18,
        option: Optional[Literal['bold', 'italic', 'underline']] = None
):
  return (font_face, font_size, option) if option is not None else (font_face, font_size)
