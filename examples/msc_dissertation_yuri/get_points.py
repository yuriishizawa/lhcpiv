import argparse
import os

import cv2

"""
function to display the coordinates of
of the points clicked on the image
"""

parsed = argparse.ArgumentParser()
parsed.add_argument("--path", type=str)
original_path = parsed.parse_args().path

path = os.getcwd() + "/" + original_path

# get first video
path = os.path.join(path, os.listdir(path)[0].split(".")[0], f"frame{'5'.zfill(6)}.jpg")

print(f"Opening image {path.split('/')[-1]}")

print(path)

# reading the image
img = cv2.imread(path, 1)

pixel_coords_path = os.path.join(original_path, "pixel_coords.txt")

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
        cv2.putText(img, str(x) + "," + str(y), (x, y), font, 1, (255, 0, 0), 2)
        cv2.imshow("image", img)

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
            str(b) + "," + str(g) + "," + str(r),
            (x, y),
            font,
            1,
            (255, 255, 0),
            2,
        )
        cv2.imshow("image", img)


# displaying the image
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.imshow("image", img)

# setting mouse hadler for the image
# and calling the click_event() function
cv2.setMouseCallback("image", click_event)

# wait for a key to be pressed to exit
cv2.waitKey(0)

# close the window
cv2.destroyAllWindows()
