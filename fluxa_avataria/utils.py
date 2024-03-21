from PIL import Image
from loguru import logger

def overlay_image(base: Image.Image, overlay_path: str) -> tuple[str, str] | None:
    """Overlays the `overlay` image on top of `base`, saving the result.

    `base`: the base (background/bottom) image.
    `overlay_path`: the path to the image to overlay on top of `base`.

    Returns the poverlaid image or `None` if errors are encountered.

    Code copied and modifed from https://gitlab.com/ASTRELION/dungeons-bot
    """
    try:
        overlay = Image.open(overlay_path)
        base.paste(overlay, (0, 0), overlay)
        return base
    except Exception as e:
        logger.error(f"Error overlaying image: {e}")
    return None