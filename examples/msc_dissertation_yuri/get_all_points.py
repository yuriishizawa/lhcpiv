import argparse
import os

import cv2

"""
function to display the coordinates of 
of the points clicked on the image
"""

parsed = argparse.ArgumentParser()
parsed.add_argument("--videos_path", type=str)
parsed.add_argument("--output_path", type=str)
original_path = parsed.parse_args().videos_path
output_path = parsed.parse_args().output_path

original_path = f"{os.getcwd()}/{original_path}"

directories_list = [
    directories
    for directories in os.listdir(original_path)
    if directories != ".DS_Store"
]

for directory in directories_list:
    # get first video
    videos_files = os.listdir(os.path.join(original_path, directory))

    first_video = list(filter(lambda x: x.endswith(".h264"), videos_files))[0].split(
        "."
    )[0]

    print(first_video)

    frame_path = os.path.join(
        original_path, directory, first_video, f"frame{'5'.zfill(6)}.jpg"
    )

    print(f"Opening image {frame_path.split('/')[-1]}")

    # reading the image
    img = cv2.imread(frame_path, 1)

    pixel_coords_path = os.path.join(output_path, f"{directory}.txt")

    with open(pixel_coords_path, "w") as f:
        f.write("")

    def click_event(event, x, y, a, b):
        # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
            # displaying the coordinates
            # on the Shell
            print(f"{x},{y}")

            with open(pixel_coords_path, "a") as f:
                f.write(f"{x},{y}\n")

            # displaying the coordinates
            # on the image window
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, f"{str(x)},{str(y)}", (x, y), font, 1, (255, 0, 0), 2)
            cv2.imshow(directory, img)

        # checking for right mouse clicks
        if event == cv2.EVENT_RBUTTONDOWN:
            # displaying the coordinates
            # on the Shell
            print(x, " ", y)

            # displaying the coordinates
            # on the image window
            font = cv2.FONT_HERSHEY_SIMPLEX
            b = img[y, x, 0]
            g = img[y, x, 1]
            r = img[y, x, 2]
            cv2.putText(
                img,
                f"{str(b)},{str(g)},{str(r)}",
                (x, y),
                font,
                1,
                (255, 255, 0),
                2,
            )
            cv2.imshow(directory, img)

    # displaying the image
    cv2.namedWindow(directory, cv2.WINDOW_NORMAL)
    cv2.imshow(directory, img)

    # setting mouse hadler for the image
    # and calling the click_event() function
    cv2.setMouseCallback(directory, click_event)

    # wait for a key to be pressed to exit
    cv2.waitKey(0)

    # close the window
    cv2.destroyAllWindows()
