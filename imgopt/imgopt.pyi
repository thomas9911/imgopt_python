from typing import Tuple

JPEG: str
JPG: str
PNG: str
SVG: str
WEBP: str

def convert(input: str, output: str) -> None: ...
def convert_explicit(input: Tuple[str, str], output: Tuple[str, str]) -> None: ...
