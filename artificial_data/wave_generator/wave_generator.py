import numpy as np
import pandas as pd

MELBOURNE_CENTER_LAT = -37.815018
MELBOURNE_CENTER_LONG = ‎144.946014

def band_function(x, x0, a, b):
    """Computes the band function."""
    return a*np.exp(-(x-x0)**2/b)
