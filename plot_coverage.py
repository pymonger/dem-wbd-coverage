#!/usr/bin/env python
import sys
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

from utils import get_tiles_from_catalog


def plot_coverage(tiles):
    """Plot coverage."""

    lons = tiles.lon
    lats = tiles.lat
    m = Basemap(projection="cyl", lon_0=0, lat_0=0, resolution='c')
    m.drawcoastlines()
    x, y = m(lons, lats)
    m.scatter(x, y, marker='o', s=1)
    plt.show()
    # plt.savefig('test.tif')


if __name__ == "__main__":
    tiles = get_tiles_from_catalog(sys.argv[1])
    plot_coverage(tiles)
