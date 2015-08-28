from numpy import *
import os
import pyhdf.SD as hdf
from osgeo import gdal, osr, _osr
from osgeo.gdalconst import GA_ReadOnly,GDT_Float32
import matplotlib.pyplot as plt
import auxil.auxil as auxil


def calculate_ndvi(GQ):
    band_RED = gdal.Open('HDF4_EOS:EOS_GRID:'+GQ+':MODIS_Grid_2D:sur_refl_b01_1',GA_ReadOnly)
    print type(band_RED)
    RED = band_RED.ReadAsArray(0,0,4800,4800).astype(float).ravel()*0.0001
    RED[RED==-2.8672]==nan
    band_NIR = gdal.Open('HDF4_EOS:EOS_GRID:'+GQ+':MODIS_Grid_2D:sur_refl_b02_1',GA_ReadOnly)
    NIR = band_NIR.ReadAsArray(0,0,4800,4800).astype(float).ravel()*0.0001
    NIR[NIR==-2.8672]==nan

#   Calculate NDVI
    NDVI = (NIR-RED)/(NIR+RED+1E-10)
    NDVI.shape = 4800,4800
    outfile = "NDVI_Sinu"
    driver = gdal.GetDriverByName( 'MEM' )
    outDataset = driver.Create(outfile,4800,4800,1,GDT_Float32)
    outDataset.GetRasterBand(1).WriteArray(NDVI)
    

#   Setting refrence system
    projInfo = band_RED.GetProjection()
    transInfo = band_RED.GetGeoTransform()
    outDataset.SetProjection(projInfo)
    outDataset.SetGeoTransform(transInfo)
    Sinu = osr.SpatialReference(projInfo)
    print "WKT format: " + str(Sinu)

#   Getting new reference system
    NAD83 = osr.SpatialReference()
    NAD83.SetWellKnownGeogCS("NAD83")
    NAD83.SetStatePlane(1501,1, "meter")
    print "WKT format: " + str(NAD83)
    

#   Transform from Sinusoidal to NAD83
    tx = osr.CoordinateTransformation ( Sinu, NAD83 )

#   Transforming
    geo_t = outDataset.GetGeoTransform()
    x_size = 4800
    y_size = 4800
    (ulx, uly, ulz ) = tx.TransformPoint(geo_t[0], geo_t[3])
    (lrx, lry, lrz ) = tx.TransformPoint( geo_t[0] + geo_t[1]*x_size, \
                                          geo_t[3] + geo_t[5]*y_size )

#   
    pixel_spacing=231.65635826
    driver = gdal.GetDriverByName( 'MEM' )
    dest = driver.Create('', int((lrx - ulx)/pixel_spacing), \
            int((uly - lry)/pixel_spacing), 1, gdal.GDT_Float32)
    print type(dest)
    
#   Calculate the new geotransform
    new_geo = ( ulx, pixel_spacing, geo_t[2], \
                uly, geo_t[4], -pixel_spacing )
    
#   Set the geotransform
    dest.SetGeoTransform( new_geo )
    dest.SetProjection ( NAD83.ExportToWkt() )

#   Resmaple
    res = gdal.ReprojectImage(outDataset, dest, Sinu.ExportToWkt(), \
                              NAD83.ExportToWkt(), gdal.GRA_Bilinear)

#   Write to disc
    driver = gdal.GetDriverByName("GTiff")
    NDVI_band = driver.CreateCopy(GQ[-45:]+"_"+"NDVI.tif", dest,0)
    NDVI_band.FlushCache()
    dest = None
    outDataset = None
