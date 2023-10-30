import datetime
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
from openpiv import filters, preprocess, pyprocess, scaling, tools, validation

from .tools import create_folder


def calculate(
    preffix_path,
    path_frame_a,
    path_frame_b,
    pixel_coords,
    real_coords,
    roi,
    winsize=32,
    searchsize=64,
    overlap=16,
    dt=1 / 25,
    threshold=1.3,
    scaling_factor=1,
    masking=False,
    masking_params=None,
    verbose=False,
    show_fig=False,
    save_fig=False,
    arrow_length=None,
    arrow_width=None,
    output_path=None,
):
    M = cv2.getPerspectiveTransform(pixel_coords, real_coords)

    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    create_folder(preffix_path + "transformed/")

    frame_a = tools.imread(preffix_path + path_frame_a)
    frame_b = tools.imread(preffix_path + path_frame_b)

    if masking:
        frame_a, _ = preprocess.dynamic_masking(frame_a, **masking_params)
        frame_b, _ = preprocess.dynamic_masking(frame_b, **masking_params)

    frame_a = cv2.warpPerspective(frame_a, M, roi)
    cv2.imwrite(preffix_path + "transformed/" + path_frame_a, frame_a)
    frame_b = cv2.warpPerspective(frame_b, M, roi)
    cv2.imwrite(preffix_path + "transformed/" + path_frame_b, frame_b)

    create_folder(preffix_path + "piv_results")

    u0, v0, sig2noise = pyprocess.extended_search_area_piv(
        frame_a.astype(np.int32),
        frame_b.astype(np.int32),
        window_size=winsize,
        overlap=overlap,
        dt=dt,
        search_area_size=searchsize,
        sig2noise_method="peak2peak",
    )

    x, y = pyprocess.get_coordinates(
        image_size=frame_a.shape, search_area_size=searchsize, overlap=overlap
    )

    u1, v1, mask = validation.sig2noise_val(  # pylint: disable=W0632
        u=u0, v=v0, s2n=sig2noise, threshold=threshold
    )

    u2, v2 = filters.replace_outliers(  # pylint: disable=W0632
        u1, v1, method="localmean", max_iter=10, kernel_size=2
    )

    x, y, u3, v3 = scaling.uniform(x, y, u2, v2, scaling_factor=scaling_factor)

    if output_path:
        create_folder(output_path)

    else:
        output_path = preffix_path + "/" + "piv_results"

    output_path = os.path.join(output_path, f"{now}.txt")
    tools.save(x, y, u3, v3, mask, output_path)

    if verbose:
        print(f"{output_path} created successfully")

    if show_fig:
        fig, ax = plt.subplots(figsize=(12, 12))
        tools.display_vector_field(
            output_path,
            ax=ax,
            scaling_factor=scaling_factor,
            scale=arrow_length,
            width=arrow_width,
            on_img=True,
            image_name=preffix_path + "transformed/" + path_frame_a,
        )

        if save_fig:
            fig.savefig(output_path.replace(".txt", ".png"))


def test_rabbit():
    print("Test rabbit")
