import numpy as np
import pytest


class DLT_2D:
    """
    Camera calibration by DLT algorithm describe by Abdel Aziz.
    """

    def __init__(self, xyz, uv):
        self.xyz = xyz
        self.uv = uv

    def Normalization(self, x):
        """
        Normalization of coordinates (centroid to the origin and mean distance of sqrt(2 or 3).
        Inputs:
        nd: number of dimensions (2 for 2D; 3 for 3D)
        x: the data to be normalized (directions at different columns and points at rows)
        Outputs:
        Tr: the transformation matrix (translation plus scaling)
        x: the transformed data
        """

        x = np.asarray(x)
        m, s = np.mean(x, 0), np.std(x)
        Tr = np.array([[s, 0, m[0]], [0, s, m[1]], [0, 0, 1]])
        Tr = np.linalg.inv(Tr)
        x = np.dot(Tr, np.concatenate((x.T, np.ones((1, x.shape[0])))))
        x = x[0:2, :].T

        return Tr, x

    def calib(self):
        """
        Camera calibration by DLT using known object points and their image points.
        This code performs 2D DLT camera calibration.
        Inputs:
        xyz are the coordinates in the object 2D space of the calibration points.
        uv are the coordinates in the image 2D space of these calibration points.
        The coordinates (x,y,z and u,v) are given as columns and the different points as rows.
        Only the first 2 columns (x and y) are used.
        There must be 4 calibrations points for the 2D DLT.
        Outputs:
        L: array of the 8 parameters of the calibration matrix
        err: error of the DLT (mean residual of the DLT transformation in units of camera coordinates).
        """

        # Convert all variables to numpy array:
        xyz = np.asarray(self.xyz)
        uv = np.asarray(self.uv)
        # number of points:
        n_p = xyz.shape[0]
        # Check the parameters:
        if uv.shape[0] != n_p:
            raise ValueError(
                "xyz (%d points) and uv (%d points) have different number of points."
                % (np, uv.shape[0])
            )
        if xyz.shape[1] != 2:
            raise ValueError(
                "Incorrect number of coordinates (%d) for 2D DLT (it should be 2)."
                % (xyz.shape[1])
            )

        # Normalize the data to improve the DLT quality (DLT is dependent of the system of coordinates).
        # This is relevant when there is a considerable perspective distortion.
        # Normalization: mean position at origin and mean distance equals to 1 at each direction.
        Txyz, xyzn = self.Normalization(xyz)
        Tuv, uvn = self.Normalization(uv)

        A = []

        for i in range(n_p):
            x, y = xyzn[i, 0], xyzn[i, 1]
            u, v = uvn[i, 0], uvn[i, 1]
            A.extend(
                (
                    [x, y, 1, 0, 0, 0, -u * x, -u * y, -u],
                    [0, 0, 0, x, y, 1, -v * x, -v * y, -v],
                )
            )
        # convert A to array
        A = np.asarray(A)
        # Find the 11 (or 8 for 2D DLT) parameters:
        _, _, Vh = np.linalg.svd(A)
        # The parameters are in the last line of Vh and normalize them:
        L = Vh[-1, :] / Vh[-1, -1]
        # Camera projection matrix:
        H = L.reshape(3, 3)
        # Denormalization:
        H = np.dot(np.dot(np.linalg.pinv(Tuv), H), Txyz)
        H = H / H[-1, -1]
        L = H.flatten("C")
        # Mean error of the DLT (mean residual of the DLT transformation in units of camera coordinates):
        uv2 = np.dot(H, np.concatenate((xyz.T, np.ones((1, xyz.shape[0])))))
        uv2 = uv2 / uv2[2, :]
        # mean distance:
        err = np.sqrt(np.mean(np.sum((uv2[0:2, :].T - uv) ** 2, 1)))

        return L, err

    def recon(self, uvs):
        """
        Reconstruction of object point from image point(s) based on the DLT parameters.
        This code performs 2D or 3D DLT point reconstruction with any number of views (cameras).
        For 3D DLT, at least two views (cameras) are necessary.
        Inputs:
        nd is the number of dimensions of the object space: 3 for 3D DLT and 2 for 2D DLT.
        nc is the number of cameras (views) used.
        Ls (array type) are the camera calibration parameters of each camera
        (is the output of DLTcalib function). The Ls parameters are given as columns
        and the Ls for different cameras as rows.
        uvs are the coordinates of the point in the image 2D space of each camera.
        The coordinates of the point are given as columns and the different views as rows.
        Outputs:
        xyz: point coordinates in space
        """

        # Convert L to array:
        Ls = np.asarray(self.calib()[0])

        # 2D and 1 camera (view), the simplest (and fastest) case
        # One could calculate inv(H) and input that to the code to speed up things if needed.
        # (If there is only 1 camera, this transformation is all Floatcanvas2 might need)
        Hinv = np.linalg.inv(Ls.reshape(3, 3))
        # Point coordinates in space:
        xyz = np.dot(Hinv, [uvs[0], uvs[1], 1])
        xyz = xyz[:2] / xyz[2]

        return xyz


class TestDLT2D:
    def test_DLTcalib(self):
        xy = [[0, 0], [0, 12.3], [14.5, 12.3], [14.5, 0]]
        uv1 = [[1302, 1147], [1110, 976], [1411, 863], [1618, 1012]]
        assert pytest.approx(DLT_2D(xy, uv1).recon(uv1[3]), abs=0.01) == xy[3]
