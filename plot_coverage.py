#!/usr/bin/env python
import sys
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd


def plot_coverage(csv_file):
    """Plot coverage."""

    map = Basemap(projection="cyl", llcrnrlat=-90, urcrnrlat=90,
                  llcrnrlon=-180, urcrnrlon=180, resolution='c')
    swbd = pd.read_csv(csv_file, header=None, names=['lat', 'lon'])
    lons = swbd.lon
    lats = swbd.lat
    m = Basemap(projection="cyl", lon_0=0, lat_0=0, resolution='c')
    m.drawcoastlines()
    x, y = map(lons, lats)
    x, y = m(lons, lats)
    m.scatter(x, y, marker='D')
    plt.show()
    plt.show()
    m = Basemap(projection="cyl", lon_0=0, lat_0=0, resolution='c')
    m.drawcoastlines()
    x, y = m(lons, lats)
    m.scatter(x, y, marker='D')
    plt.show()


if __name__ == "__main__":
    plot_coverage(sys.argv[1])
