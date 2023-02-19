import cv2
from streamlit import title,  button, image, columns
from datetime import datetime

title('Motion Detector')

left_column, right_column = columns(2)

with left_column:
    start_button_pressed = button('Start Camera')

with right_column:
    close_button_pressed = button('Close Camera')

if start_button_pressed:
    streamlit_image = image([])

    camera = cv2.VideoCapture(0)

    while True:

        if close_button_pressed:
            break

        check, original_frame = camera.read()

        frame_with_rgb = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)

        current_time = datetime.now()

        # org is the coordinate from the top left corner
        cv2.putText(
            img=frame_with_rgb,
            text=current_time.strftime('%A'),
            org=(50, 60),
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=3,
            color=(255, 255, 255),
            thickness=2,
            lineType=cv2.LINE_AA
        )

        cv2.putText(
            img=frame_with_rgb,
            text=current_time.strftime('%H:%M:%S'),
            org=(50, 120),
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=3,
            color=(255, 0, 0),
            thickness=2,
            lineType=cv2.LINE_AA
        )

        streamlit_image.image(frame_with_rgb)

    camera.release()