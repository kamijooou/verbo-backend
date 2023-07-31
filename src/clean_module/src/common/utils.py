import numpy as np
from PIL import Image, ImageFilter


def border_std_deviation(base: Image, mask: Image, off_white_threshold: int=240) -> tuple[float, int]:
    """
    Calculate the border uniformity of a mask.
    For this, find the edge pixels of the mask and then calculate the median color of the pixels around them.
    Also calculate the standard deviation of the colors around the edge pixels.
    In case the mask is blank, return a very high standard deviation.
    :raises BlankMaskError: If one or more masks are blank, meaning that the box is not valid.
    :param base: The base image. Mode: "L"
    :param mask: The mask to calculate the border uniformity of. Mode: "1"
    :param off_white_threshold: The threshold for a pixel to be considered off-white.
    :return: The border uniformity as the standard deviation and the median color of the border.
    """
    # Transform the mask into its edge pixels.
    mask = mask.filter(ImageFilter.FIND_EDGES)
    # Collect all pixels from the base image where the mask has a value of 1.
    # Use numpy for efficiency.
    base_data = np.array(base)
    mask_data = np.array(mask)

    border_pixels = base_data[mask_data == 255]
    # Calculate the number of pixels in the border.
    num_pixels = len(border_pixels)
    if num_pixels == 0:
        # We received an empty mask.
        return None, None
    # Calculate the standard deviation of the border pixels.
    std = float(np.std(border_pixels))
    # Get the average color of the border pixels, round to highest integer.
    median_color = int(np.median(border_pixels))
    # logger.debug(f"Border uniformity: {std} ({num_pixels} pixels), median color: {median_color}")
    # Round up any color over the threshold to 255. This should prevent slight off-white colors from sneaking in.
    if median_color > off_white_threshold:
        median_color = 255

    return std, median_color
