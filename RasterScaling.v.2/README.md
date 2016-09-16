This tool reads an excel file that contains the scaling factor for a raster and 
finds the appropriate raster to multiply with the proper scaling factor.
e.g.
In the input solar radiation raster folder there are 154 esri grid raster that represent the 154 days of any year and the corresponding 
excel scaling factor file contains the scale factor for those 154 days for multiple year. So now using this tool you can create solar radiation raster for
all the years in the excel file and this raster for each 154 days.

Say raster name in 0512 i.e. May 12 say again excel file has two years 1912 and 1913
So now you can generate two raster for May 12 for both 1912 and 1913.

This script takes  inputs as below
>>1. Input raster folder
>>2. Input excel file path - needs to be exactly formatted as attached
>>3. Output raster folder
>>4. Temporary folder




==================================================

Email: msi_g@yahoo.com

Writer/Developer: sharifulgeo

Created on 16 september, 2016

N.B. This tool is tested against feature class and projected coordinate system