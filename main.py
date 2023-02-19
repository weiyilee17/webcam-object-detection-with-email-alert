import cv2
from time import sleep

# 0 means the main camera. For laptops, that is the integrated one
video = cv2.VideoCapture(0)

# Give the camera some time to load
sleep(1)

first_frame = None

while True:
    check, original_frame = video.read()

    # Convert to gray scale because it's inefficient to compare against the original image with RGB 3 channels
    gray_scaled_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)

    # Further filter out noise with Gaussian Blur. (21, 21) being the Gaussian Kernel size, should be odd values
    # the larger the value, the more blur the image turns out to be.
    # 0 is the kernel standard deviation for x-axis
    gray_scaled_frame_blurred = cv2.GaussianBlur(gray_scaled_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_scaled_frame_blurred

    delta_frame = cv2.absdiff(first_frame, gray_scaled_frame_blurred)

    # There are noises in delta_frame, even if there is no obvious differences happening
    # To improve efficiency, we apply threshold to values, so differences above 60 would be assigned 255, else 0
    # So small values like 3, 8, 15... would be neglected
    # The threshold value 60, would be one that comes out by trial and error. It depends on where your camera is.
    threshold_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]

    # After threshold (erosion), the white parts are smaller, because they used to be small values, now they are all
    # filtered to black, so things look smaller in this frame. Dilation tries to make the things bigger, as it
    # originally was. The second argument None is for configuration that we don't need for simplicity
    dilation_frame = cv2.dilate(threshold_frame, None, iterations=2)

    contours, hierarchy = cv2.findContours(dilation_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for single_contour in contours:
        # if single_contour is a fake object(background light differences)
        # 5000 is a value that comes from trial and error
        if cv2.contourArea(single_contour) < 5_000:
            continue

        # x, y being the coordinates of the top left point of the rectangle
        x, y, width, height = cv2.boundingRect(single_contour)

        # Third argument being the color of the rectangle, forth being the width
        cv2.rectangle(original_frame, (x, y), (x + width, y + height), (0, 255, 0), 3)

    cv2.imshow('MacBook Pro Camera', original_frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()
