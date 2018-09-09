import numpy as np

MELBOURNE_CENTER_LAT = -37.815018
MELBOURNE_CENTER_LONG = 144.946014

BAND_FUNCTION_DEFAULT_SCALAR = 100
BAND_FUNCTION_DEFAULT_TIMECONST = 10

X0_START = 0  # Starts at the center of the city
X0_SCALAR_CONST = 10  # Rate at which the x0 shifts

def band_function(x, x0, a=BAND_FUNCTION_DEFAULT_SCALAR, b=BAND_FUNCTION_DEFAULT_TIMECONST):
    """Computes the band function."""
    return a*np.exp(-(x-x0)**2/b)


def x0_func(t):
    """Moves the x0 over time. `t` is the year."""
    return X0_START + X0_SCALAR_CONST*(t-2000)


def relativevector2latlon(vec):
    """Turns a relative vector (x, y) into (lat, long) tuple."""
    x, y = vec
    lat = MELBOURNE_CENTER_LAT + float(y)/111111
    lon = MELBOURNE_CENTER_LONG + float(x)/(111111*np.cos(MELBOURNE_CENTER_LAT))
    return (lat, lon)


def generate_markers(year):
    """Creates a list of markers for the ingestion of the fake data."""
    markers = []
    for deg in np.linspace(0, 2*np.pi, 360):  # Equates to 1/2 degree steps
        unit_vector = (np.cos(deg), np.sin(deg))
        for x_step in np.linspace(0, 1e4, 100):
            band_output = band_function(x_step, x0_func(year))
            marker_coord = relativevector2latlon((
                unit_vector[0]*x_step,
                unit_vector[1]*x_step
            ))
            [markers.append(marker_coord) for _ in range(int(band_output))]
    return markers


if __name__ == '__main__':
    markers = generate_markers(2020)
    print(markers[0], markers[int(len(markers)*0.5)])
