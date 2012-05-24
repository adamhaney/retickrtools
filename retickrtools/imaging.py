"""
imaging.py should contain any imaging-related tools that Retickr might need to
use.

@author: Cory Walker
@organization: Retickr
@contact: cory.walker@retickr.com

"""

from PIL import Image

def round_corners(image_f, save_f, size=(48, 48), mask_fn="imaging_round_mask.png"):
    """Generates an icon of the specified size with the specified rounding mask.

    Arguments:
    image_f -- A file object for the image. Can be a file or StringIO, etc.
    save_f -- A file object for the saved icon. Can be a file or StringIO, etc.
    size -- Size to scale to before applying the mask. (default (48, 48))
    mask_fn -- Rounding mask name to apply. (default "imaging_round_mask.png")

    """

    x, y = size
    im = Image.open(image_f)

    # This will scale to the (x, y), but not crop:
    im = im.resize((x, y), Image.ANTIALIAS)

    # Load and apply our mask. White opaque, black transparent
    # See: http://stackoverflow.com/questions/890051/how-do-i-generate-circuar-thumbnails-with-pil
    mask = Image.open(mask_fn).convert('L')
    im.putalpha(mask)

    # Save our hard work. git r dun
    im.save(save_f, "PNG")
