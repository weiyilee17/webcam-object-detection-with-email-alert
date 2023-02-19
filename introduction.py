# Can't use from cv2 import imread, seems to be because the __init__.py file has an empty array for __all__
# Could be fixed by downgrading to 4.5.3.56, but not sure whether I should do that
import cv2
from numpy import array

# image is a numpy ndarray, each pixel is represented in an array, B, G, R
image = cv2.imread('image.png')

# The shape property returns a tuple of (vertical_pixels_count, horizontal_pixels_count, channels_count)
print(image.shape)

new_image = array([
    [
        [0, 0, 255],
        [255, 255, 255],
        [255, 255, 255],
        [187, 41, 160],
    ],
    [
        [255, 255, 255],
        [255, 255, 255],
        [255, 255, 255],
        [255, 255, 255],
    ],
    [
        [255, 255, 255],
        [0, 0, 0],
        [47, 255, 173],
        [255, 255, 255],
    ]
])

cv2.imwrite('new_image.png', new_image)
