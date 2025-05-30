from PIL import Image
import io
import base64
from typing import Literal


def read_base64_image(base64_image: str) -> Image.Image:
    """Read a base64 encoded image string and return a PIL Image object."""
    return Image.open(io.BytesIO(base64.b64decode(base64_image)))


def encode_base64_image(image: Image.Image, format: Literal['PNG', 'JPEG'] = 'JPEG') -> str:
    """Convert a PIL Image object to a base64 encoded string."""
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def resize_longest_edge(image: Image.Image, longest_edge: int = 512):
    """Resize the image to have the longest edge of the specified length while maintaining the aspect ratio."""
    width, height = image.size
    if width > height:
        new_width = longest_edge
        new_height = round((new_width / width) * height)
    else:
        new_height = longest_edge
        new_width = round((new_height / height) * width)
    return image.resize((new_width, new_height))
