import re
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
from gdalconst import GA_ReadOnly

from isceobj.Image import createDemImage


gdal.UseExceptions()


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


def generate_swbd_fill(srtm_file, swbd_file):
    """Create SWBD fill tile with all land."""

    srtm_ds = gdal.Open(srtm_file, GA_ReadOnly)
    gt = srtm_ds.GetGeoTransform()
    cols = srtm_ds.RasterXSize
    rows = srtm_ds.RasterYSize
    #print("gt: {}".format(gt))
    #print("cols: {}".format(cols))
    #print("rows: {}".format(rows))
    metadata = srtm_ds.GetMetadata()
    #print("metadata: {}".format(metadata))
    
    
    srtm_band = srtm_ds.GetRasterBand(1)
    #print("srtm_band: {}".format(srtm_band))
    data = srtm_band.ReadAsArray()
    #print("data: {}".format(data))
    no_data_value = srtm_band.GetNoDataValue()
    #print("no_data_value: {}".format(no_data_value))
    unit_type = srtm_band.GetUnitType()
    #print("unit_type: {}".format(unit_type))
    
    new_data = np.zeros(data.shape, np.int8)
    #print("new_data: {}".format(new_data))
    #print("new_data.shape: {}".format(new_data.shape))
    
    swbd_ds = gdal.GetDriverByName('ISCE').Create(swbd_file, cols, rows, 1, gdal.GDT_Byte)
    swbd_ds.SetGeoTransform(gt)
    swbd_ds.SetMetadata(metadata)
    swbd_band = swbd_ds.GetRasterBand(1)
    swbd_band.SetNoDataValue(no_data_value)
    swbd_band.SetUnitType(unit_type)
    swbd_band.WriteArray(new_data)
    swbd_srs = osr.SpatialReference()
    swbd_srs.ImportFromWkt(srtm_ds.GetProjectionRef())
    swbd_ds.SetProjection(swbd_srs.ExportToWkt())
    swbd_band.FlushCache()

    srtm_ds = None
    swbd_ds = None
