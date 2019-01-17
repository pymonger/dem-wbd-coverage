#!/usr/bin/env python
import sys
import re
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd


TILE_RE = re.compile(
    r'^(?P<lat_orient>N|S)(?P<lat>\d+)(?P<lon_orient>E|W)(?P<lon>\d+)')


def get_tiles_from_catalog(catalog_file):
    """Parse catalog of tiles and return pandas data frame of
       tile locations."""

    lats = []
    lons = []
    with open(catalog_file) as f:
        for line in f:
            match = TILE_RE.search(line)
            if not match:
                raise(RuntimeError("Failed to extract tile info: {}".format(line)))
            m = match.groupdict()
            lats.append(-int(m['lat']) if m['lat_orient']
                        == 'S' else int(m['lat']))
            lons.append(-int(m['lon']) if m['lon_orient']
                        == 'W' else int(m['lon']))
    return pd.DataFrame({'lat': lats, 'lon': lons})


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
