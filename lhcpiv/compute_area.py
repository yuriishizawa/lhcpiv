import matplotlib.pyplot as plt
import numpy as np


class compute_area:
    """
    compute_area é uma classe utilizada no cálculo da seção transversal de canais hidráulicos.
    """

    def __init__(self, df):
        self.df = df

    def area(self):
        A = []
        for i in list(range(len(self.df.depth))):
            if i == 0 or i == 1 or i == len(self.df.depth) - 1:
                A.append(0)
            else:
                A.append(
                    round(
                        (self.df.dist_left_bank[i] - self.df.dist_left_bank[i - 1])
                        * 0.5
                        * (self.df.depth[i - 1] + self.df.depth[i]),
                        3,
                    )
                )

        return A

    def pm(self):
        Pm = []
        for i in list(range(len(self.df.depth))):
            if i == 0 or i == 1 or i == len(self.df.depth) - 1:
                Pm.append(0)
            elif i == 2:
                Pm.append(
                    round(
                        self.df.depth[i - 1]
                        + np.sqrt(
                            (self.df.depth[i - 1] - self.df.depth[i]) ** 2
                            + (
                                self.df.dist_left_bank[i]
                                - self.df.dist_left_bank[i - 1]
                            )
                            ** 2
                        ),
                        3,
                    )
                )
            elif i == len(self.df.depth) - 2:
                Pm.append(
                    round(
                        self.df.depth[i]
                        + np.sqrt(
                            (self.df.depth[i - 1] - self.df.depth[i]) ** 2
                            + (
                                self.df.dist_left_bank[i]
                                - self.df.dist_left_bank[i - 1]
                            )
                            ** 2
                        ),
                        3,
                    )
                )
            else:
                Pm.append(
                    round(
                        np.sqrt(
                            (self.df.depth[i - 1] - self.df.depth[i]) ** 2
                            + (
                                self.df.dist_left_bank[i]
                                - self.df.dist_left_bank[i - 1]
                            )
                            ** 2
                        ),
                        3,
                    )
                )
        return Pm

    def Rh(self):
        return sum(self.area()) / sum(self.pm())

    def plot(self):
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
