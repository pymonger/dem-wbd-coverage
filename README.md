# dem-wbd-coverage
Utility to display DEM or WBD tile coverage

## Requirements
- Anaconda Python 3
- basemap
- pandas
- geos
- awscli
- e.g.
  ```
  conda install basemap pandas geos
  conda install -c conda-forge awscli
  ```
- export *PROJ_LIB*:
  ```
  export PROJ_LIB=${HOME}/anaconda3/pkgs/proj4-5.2.0-h1de35cc_1001/share/proj
  ```

## Download catalog of tiles
1. Set bucket:
   ```
   export BUCKET=s3://grfn-v2-ops-product-bucket
   ```
1. Get catalog of tiles for SRTM1_v3:
   ```
   aws s3 ls ${BUCKET}/datasets/dem/SRTM1_v3/ | awk '{print $4}' | grep -v '^\.' > SRTM1_v3.txt
   ```
1. Get catalog of tiles for NED1:
   ```
   aws s3 ls ${BUCKET}/datasets/dem/ned1/ | awk '{print $4}' | grep -v '^\.' > NED1.txt
   ```
1. Get catalog of tiles for NED13:
   ```
   aws s3 ls ${BUCKET}/datasets/dem/ned13/ | awk '{print $4}' | grep -v '^\.' > NED13.txt
   ```
1. Get catalog of tiles for SRTM WBD:
   ```
   aws s3 ls ${BUCKET}/datasets/dem/usgs_mirror/SRTMSWBD.003/2000.02.11/ | awk '{print $4}' | grep -v '^\.' | grep -v .zip.xml > SWBD.txt
   ```

## View tile coverage
```
./plot_coverage.py <catalog file>
```
For example:
```
./plot_coverage.py SRTM1_v3.txt
```

## View tile coverage differences
```
./diff_coverage.py <catalog file 1> <catalog file 2>
```
For example:
```
./diff_coverage.py SRTM1_v3.txt SWBD.txt
```
To dump out a csv of the differences, add a third arg:
```
./diff_coverage.py <catalog file 1> <catalog file 2> <output csv file>
```
For example:
```
./diff_coverage.py SRTM1_v3.txt SWBD.txt dem_wbd_diff.csv
```

## Generate SWBD tile fills (all land) where SRTM exists but not SWBD
```
./generate_fills.py <SRTM catalog file> <SWBD catalog file> <SRTM root url>
```
For example:
```
./generate_fills.py SRTM1_v3.txt SWBD.txt s3://hysds-v2-dev-product-bucket/datasets/dem/SRTM1_v3
```
