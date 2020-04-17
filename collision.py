import numpy as np


def check_collision(point, center, radius):
    dist = np.sqrt(
        (center[0] - point[0]) ** 2
        + (center[1] - point[1]) ** 2
    )

    if dist < radius:
        return True
    else:
        return False