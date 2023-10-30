# Importing packages
import argparse
import os

import cv2


def vf(path_to_video, qty_frames, x1=None, x2=None, y1=None, y2=None, rotate=False):
    """
    Create frames in format jpg from videos.
    """
    video_format = path_to_video.split(".")[-1]
    # Read the video from specified path
    cam = cv2.VideoCapture(path_to_video)

    try:
        folder_name = path_to_video.replace(f".{video_format}", "")
        # creating a folder named data
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"Created folder {folder_name}")

    # if not created then raise error
    except OSError:
        print("Error: Creating directory of data")

    # frame
    currentframe = 0

    while True:
        # reading from frame
        ret, frame = cam.read()

        if ret and currentframe < qty_frames and currentframe > 3:
            # if video is still left continue creating images
            name = f"./{folder_name}/frame{str(currentframe).zfill(6)}.jpg"

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if x1 is None:
                x1 = 0
            if x2 is None:
                x2 = frame.shape[1]

            if y1 is None:
                y1 = 0
            if y2 is None:
                y2 = frame.shape[0]

            frame = frame[y1:y2, x1:x2]

            if rotate:
                frame = cv2.rotate(frame, cv2.ROTATE_180)

            # writing the extracted images
            cv2.imwrite(name, frame)

            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1

        elif currentframe <= 4:
            currentframe += 1
        else:
            print("Success")
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()


def main(path, qty_frames, x1=None, x2=None, y1=None, y2=None, rotate=False):
    vf(path, qty_frames, x1, x2, y1, y2, rotate)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str)
    parser.add_argument("--qty_frames", type=int, default=10)
    parser.add_argument("--x1", type=int, default=None)
    parser.add_argument("--x2", type=int, default=None)
    parser.add_argument("--y1", type=int, default=None)
    parser.add_argument("--y2", type=int, default=None)
    parser.add_argument("--rotate", type=bool, default=False)
    parsed = parser.parse_args()

    main(
        path=parsed.path,
        qty_frames=parsed.qty_frames,
        x1=parsed.x1,
        x2=parsed.x2,
        y1=parsed.y1,
        y2=parsed.y2,
        rotate=parsed.rotate,
    )
