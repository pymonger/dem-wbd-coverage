#!/usr/bin/env python
import os
import sys

from utils import get_tiles_from_catalog, generate_swbd_fill


def generate_fills(srtm_tiles, swbd_tiles, srtm_tiles_url):
    """Generate fills."""

    for index, row in srtm_tiles.iterrows():
        # tile exists in srtm_tiles but not in swbd_tiles
        exists = ((swbd_tiles['lat'] == row['lat']) & (
            swbd_tiles['lon'] == row['lon'])).any()
        if not exists:
            if row['lat'] >= 0: lat = "N{:02d}".format(row['lat'])
            else: lat = "S{:02d}".format(abs(row['lat']))
            if row['lon'] >= 0: lon = "E{:03d}".format(row['lon'])
            else: lon = "W{:03d}".format(abs(row['lon']))
            url = "{}/{}{}.hgt.zip".format(srtm_tiles_url, lat, lon)
            os.system("aws s3 cp {} .".format(url))
            srtm_file = os.path.basename(url)
            swbd_file = "{}{}.SRTMSWBD.raw".format(lat, lon)
            generate_swbd_fill(srtm_file, swbd_file)
            os.system("zip {}.zip {}*".format(swbd_file, swbd_file))
            os.unlink(srtm_file)
          

if __name__ == "__main__":
    srtm_tiles = get_tiles_from_catalog(sys.argv[1])
    swbd_tiles = get_tiles_from_catalog(sys.argv[2])
    srtm_tiles_url = sys.argv[3]
    generate_fills(srtm_tiles, swbd_tiles, srtm_tiles_url)
