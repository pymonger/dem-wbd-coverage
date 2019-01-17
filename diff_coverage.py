#!/usr/bin/env python
import sys
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

from utils import get_tiles_from_catalog


def diff_coverage(tiles1, tiles2, csv=None):
    """Diff coverage."""

    df = pd.DataFrame(columns=('lat', 'lon'))
    for index, row in tiles1.iterrows():
        # tile exists in tiles1 but not in tiles2
        exists = ((tiles2['lat'] == row['lat']) & (
            tiles2['lon'] == row['lon'])).any()
        if not exists:
            df = df.append({
                'lat': row['lat'],
                'lon':  row['lon'],
            }, ignore_index=True)

    # dump results to csv
    if csv is not None:
        df.to_csv(csv, index=False)

    # display plot
    m = Basemap(projection="cyl", lon_0=0, lat_0=0, resolution='c')
    m.drawcoastlines()
    x, y = m(df.lon, df.lat)
    m.scatter(x, y, marker='o', s=1)
    plt.show()


if __name__ == "__main__":
    tiles1 = get_tiles_from_catalog(sys.argv[1])
    tiles2 = get_tiles_from_catalog(sys.argv[2])
    diff_coverage(tiles1, tiles2, sys.argv[3] if len(sys.argv) >= 4 else None)
