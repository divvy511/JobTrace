from PIL import Image

def downscale_image(image: Image.Image, max_width: int) -> Image.Image:
    if image.width <= max_width:
        return image

    ratio = max_width / image.width
    new_height = int(image.height * ratio)
    return image.resize((max_width, new_height), Image.BILINEAR)
