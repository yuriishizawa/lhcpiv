import pytest
from gekko import GEKKO


def calculate(dists):
    """
    Function to calculate coordinates of a rectangule given the distance between points
    Inputs:
    dists: distances from a to b, b to c, c to d, d to a, a to c and b to d.
    Outputs:
    xa, ya, xb, yb, xc, yc, xd, yd: coordinates of the rectangule.
    """

    # xa, ya = 0, 0
    xa, ya, yb = 0, 0, 0
    m = GEKKO()
    # dab = m.Const(dists[0], "dab")
    dbc = m.Const(dists[1], "dbc")
    dcd = m.Const(dists[2], "dcd")
    dda = m.Const(dists[3], "dda")
    dac = m.Const(dists[4], "dac")
    dbd = m.Const(dists[5], "dbd")
    # xb, yb, xc, yc, xd, yd = [m.Var(value=0) for i in range(6)]
    xb, xc, yc, xd, yd = [m.Var(value=0) for _ in range(5)]
    m.Equations(
        [
            # xb ** 2 + yb ** 2 == dab ** 2,
            xc**2 + yc**2 == dac**2,
            xd**2 + yd**2 == dda**2,
            (xb - xd) ** 2 + (yb - yd) ** 2 == dbd**2,
            (xd - xc) ** 2 + (yd - yc) ** 2 == dcd**2,
            (xb - xc) ** 2 + yc**2 == dbc**2,
            # xb >= 0,
            xc >= 0,
            yc >= 0,
            yd >= 0,
        ]
    )
    m.solve(disp=False)
    return [(xa, ya), (xb[0], yb), (xc[0], yc[0]), (xd[0], yd[0])]


class Testdist_to_coords:
    def test_calculate(self):
        dists = [3, 1, 3.0, 1, 10**0.5, 10**0.5]
        assert pytest.approx(calculate(dists), abs=0.01) == [
            (0, 0),
            (3, 0),
            (1, 3),
            (0, 1),
        ]


if __name__ == "__main__":
    print(calculate([3, 1, 3.0, 1, 10**0.5, 10**0.5]))
