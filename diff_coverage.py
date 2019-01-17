#!/usr/bin/env python
import sys
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

from utils import get_tiles_from_catalog


def diff_coverage(tiles1, tiles2):
    """Diff coverage."""

    lats = []
    lons = []
    for index, row in tiles1.iterrows():
        exists = ((tiles2['lat'] == row['lat']) & (
            tiles2['lon'] == row['lon'])).any()
        if not exists:
            #print(row['lat'], row['lon'])
            lats.append(row['lat'])
            lons.append(row['lon'])
    m = Basemap(projection="cyl", lon_0=0, lat_0=0, resolution='c')
    m.drawcoastlines()
    x, y = m(lons, lats)
    m.scatter(x, y, marker='o', s=1)
    plt.show()


if __name__ == "__main__":
    tiles1 = get_tiles_from_catalog(sys.argv[1])
    tiles2 = get_tiles_from_catalog(sys.argv[2])
    diff_coverage(tiles1, tiles2)
