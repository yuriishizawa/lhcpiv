"""
The `compute_area` module contains the `ComputeArea` class, which is used to
calculate the cross-sectional area of hydraulic channels.

The `ComputeArea` class contains the following methods:

- `__init__(self, df)`: The constructor method takes a pandas DataFrame `df` as
input and initializes the `df` attribute of the class.
- `area(self)`: This method calculates the cross-sectional area of the hydraulic
channel at each point in the DataFrame `df`. It returns a list of the calculated
areas.
- `pm(self)`: This method calculates the wetted perimeter of the hydraulic
channel at each point in the DataFrame `df`. It returns a list of the calculated
wetted perimeters.
- `Rh(self)`: This method calculates the hydraulic radius of the channel by
dividing the total cross-sectional area by the total wetted perimeter. It returns
the calculated hydraulic radius.
- `plot(self)`: This method generates a plot of the hydraulic channel using the
data in the DataFrame `df`. It returns the generated plot.
"""

from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class ComputeArea:
    """
    compute_area é uma classe utilizada no cálculo da seção transversal de canais hidráulicos.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_area(self) -> List[float]:
        """
        This method calculates the cross-sectional area of the
        hydraulic channel at each point in the DataFrame `df`.
        It returns a list of the calculated areas.

        Parameters
        ----------
        self : ComputeArea
            The ComputeArea object.

        Returns
        -------
        List[float]
            A list of the calculated cross-sectional areas.
        """
        area = []
        for index, depth in enumerate(self.df.depth):
            if index in (0, 1, len(self.df.depth) - 1):
                area.append(0)
            else:
                area.append(
                    round(
                        (
                            self.df.dist_left_bank[index]
                            - self.df.dist_left_bank[index - 1]
                        )
                        * 0.5
                        * (self.df.depth[index - 1] + depth),
                        3,
                    )
                )

        return area

    def get_wetted_perimeter(self) -> List[float]:
        """
        This method calculates the wetted perimeter of the
        hydraulic channel at each point in the DataFrame `df`.
        It returns a list of the calculated wetted perimeters.

        Parameters
        ----------
        self : ComputeArea
            The ComputeArea object.

        Returns
        -------
        List[float]
            A list of the calculated wetted perimeters.
        """
        wetted_perimeter = []
        for i, (depth, dist_left_bank) in enumerate(
            zip(self.df.depth, self.df.dist_left_bank)
        ):
            if i == 0 or i == len(self.df.depth) - 1:
                wetted_perimeter.append(0)
            else:
                dx = dist_left_bank - self.df.dist_left_bank[i - 1]
                dy = depth - self.df.depth[i - 1]
                wetted_perimeter.append(round(np.sqrt(dx**2 + dy**2), 3))
        return wetted_perimeter

    def get_hydraulic_radius(self) -> float:
        """
        This method calculates the hydraulic radius of the channel by
        dividing the total cross-sectional area by the total wetted perimeter.
        It returns the calculated hydraulic radius.

        Parameters
        ----------
        self : ComputeArea
            The ComputeArea object.

        Returns
        -------
        float
            The calculated hydraulic radius.
        """
        return sum(self.get_area()) / sum(self.get_wetted_perimeter())

    def plot_profile(self) -> None:
        """Plots the depth profile of the river cross-section."""
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.df.dist_left_bank, self.df.depth, color="black")
        ax.plot([0, self.df.dist_left_bank.max()], [0, 0], color="blue")
        ax.fill_between(self.df.dist_left_bank, self.df.depth, color="cyan", alpha=0.4)
        ax.set_aspect(aspect=1)
        for i in list(range(len(self.df))):
            plt.plot(
                [self.df.dist_left_bank[i], self.df.dist_left_bank[i]],
                [0, self.df.depth[i]],
                color="black",
            )
        plt.xticks(self.df.dist_left_bank)
        plt.xlabel("Distance from the left bank (m)")
        plt.ylabel("Depth (m)")
        plt.gca().invert_yaxis()
