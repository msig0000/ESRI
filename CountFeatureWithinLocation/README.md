This tool calculates/counts the existence of another feature within a define extent of enclosure of the first feature and saves this result in a field , given in the tool parameter by user, of the first feature.

>>>>This is written in response of POINTS IN POLYGON tool in QGIS 

This script takes five inputs as below

>>1. Workspace (folder):The workspace where all calculation to be done
>>2. Input Feature (Feature Layer):The input feature of which extent is considered for counting other feature
>>3. Count Feature (Feature Layer) :The feature of which existence in the extent of Input feature to be counted
>>4. Count Field Name (String) :The field name of INPUT feature where count to be stored. Firstly a field to be created in the attribute table of the INPUT feature and stored afterwards
>>5. Search Radius (Linear unit) :The search extent of the INPUT feature where COUNT feaure will be searched


![alt tag](http://i.imgur.com/L8XwCJ1.png)



>>>>This tool is tested against shapefile and projected coordinate system with ArcGIS Advanced License




==================================================

Email: msi_g@yahoo.com



Created on 13 June, 2015

N.B. This tool is tested against shapefile and projected coordinate system
