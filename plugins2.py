"""
Plugin utilities for the pictool.

Each function here is a valid plug-in. To be valid, a function must:
- Accept an image buffer (2D list of RGB objects) as the first argument
- Have default values for all other parameters
- Return True if it modifies the image and False if it doesn't

Author: Ian Ifill
Date: June 9, 2025
"""

from rgb import RGB
import math
import random

def display(image):
    """
    Returns False after printing all pixels in a readable format.
    Does not modify the image.
    """
    height = len(image)
    width  = len(image[0])
    maxsize = max(len(repr(pixel)) for row in image for pixel in row)

    print()
    for r, row in enumerate(image):
        for c, pixel in enumerate(row):
            middle = repr(pixel)
            padding = maxsize - len(middle)

            prefix = '      '
            if r == 0 and c == 0:
                prefix = '[  [  '
            elif c == 0:
                prefix = '   [  '

            suffix = ','
            if r == height - 1 and c == width - 1:
                suffix = ' ' * padding + ' ]  ]'
            elif c == width - 1:
                suffix = ' ' * padding + ' ],'

            print(prefix + middle + suffix)
    return False

def dered(image):
    """
    Returns True after removing all red from the image.
    """
    for row in image:
        for pixel in row:
            pixel.red = 0
    return True

def mono(image, sepia=False):
    """
    Converts the image to grayscale or sepia.
    """
    for row in image:
        for pixel in row:
            brightness = 0.3 * pixel.red + 0.6 * pixel.green + 0.1 * pixel.blue
            if sepia:
                pixel.red = int(brightness)
                pixel.green = int(0.6 * brightness)
                pixel.blue = int(0.4 * brightness)
            else:
                gray = int(brightness)
                pixel.red = gray
                pixel.green = gray
                pixel.blue = gray
    return True

def flip(image, vertical=False):
    """
    Flips the image horizontally (default) or vertically.
    """
    if vertical:
        image.reverse()
    else:
        for row in image:
            row.reverse()
    return True

def transpose(image):
    """
    Transposes the image (swap rows and columns).
    """
    if not image or not image[0]:
        return True
    rows = len(image)
    cols = len(image[0])
    transposed = [[image[r][c] for r in range(rows)] for c in range(cols)]
    image.clear()
    image.extend(transposed)
    return True

def rotate(image, right=False):
    """
    Rotates the image 90 degrees left or right.
    """
    if right:
        flip(image, vertical=True)
        transpose(image)
    else:
        transpose(image)
        flip(image, vertical=True)
    return True

def vignette(image):
    """
    Darkens the corners of the image using a vignette effect.
    """
    height = len(image)
    width = len(image[0])
    center_row = height // 2
    center_col = width // 2
    H = math.sqrt(center_row**2 + center_col**2)

    for r in range(height):
        for c in range(width):
            d = math.sqrt((r - center_row)**2 + (c - center_col)**2)
            factor = 1 - (d / H)**2
            pixel = image[r][c]
            pixel.red   = round(pixel.red * factor)
            pixel.green = round(pixel.green * factor)
            pixel.blue  = round(pixel.blue * factor)
    return True

def blur(image, radius=5):
    """
    Applies a box blur to the image using a copy of original pixels.
    """
    height = len(image)
    width = len(image[0])
    original = [[RGB(p.red, p.green, p.blue, p.alpha) for p in row] for row in image]

    for r in range(height):
        for c in range(width):
            row_min = max(0, r - radius)
            row_max = min(height - 1, r + radius)
            col_min = max(0, c - radius)
            col_max = min(width - 1, c + radius)

            total_red = total_green = total_blue = total_alpha = count = 0

            for i in range(row_min, row_max + 1):
                for j in range(col_min, col_max + 1):
                    p = original[i][j]
                    total_red += p.red
                    total_green += p.green
                    total_blue += p.blue
                    total_alpha += p.alpha
                    count += 1

            image[r][c] = RGB(
                round(total_red / count),
                round(total_green / count),
                round(total_blue / count),
                round(total_alpha / count)
            )
    return True

def pixellate(image, step=10):
    """
    Applies a pixelation effect to the image using step x step blocks.
    """
    height = len(image)
    width = len(image[0])

    for row in range(0, height, step):
        for col in range(0, width, step):
            row_max = min(row + step, height)
            col_max = min(col + step, width)
            total_red = total_green = total_blue = total_alpha = count = 0

            for r in range(row, row_max):
                for c in range(col, col_max):
                    p = image[r][c]
                    total_red += p.red
                    total_green += p.green
                    total_blue += p.blue
                    total_alpha += p.alpha
                    count += 1

            avg_pixel = RGB(
                round(total_red / count),
                round(total_green / count),
                round(total_blue / count),
                round(total_alpha / count)
            )

            for r in range(row, row_max):
                for c in range(col, col_max):
                    image[r][c] = avg_pixel
    return True

def scramble(image, amount=500):
    """
    Randomly changes a number of pixels in the image.
    """
    height = len(image)
    width = len(image[0])

    for _ in range(amount):
        r = random.randint(0, height - 1)
        c = random.randint(0, width - 1)
        pixel = image[r][c]
        image[r][c] = RGB(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            pixel.alpha
        )
    return True

def brighten(image, factor=1.25):
    """
    Brightens the image by multiplying RGB values by a factor (max 255).
    """
    for row in image:
        for pixel in row:
            pixel.red   = min(round(pixel.red * factor), 255)
            pixel.green = min(round(pixel.green * factor), 255)
            pixel.blue  = min(round(pixel.blue * factor), 255)
    return True