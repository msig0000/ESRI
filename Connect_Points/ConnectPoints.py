# 
# This tools generates spider netwok based on the set search radius.
#This script creates some temporary file and folder (C:\temp) which will be deleted when script completes.
#This script takes three inputs as below
#>>1. Input Point Feature (file)
#>>2. Output workspace(folder)
#>>3. Output feature name(string)
#>>4. Search radius (linear unit-double)
#email: msi_g@yahoo.com
#Writer: Shariful Islam

#=====================Do imports=============================#
import arcpy,os,sys,shutil
from arcpy import env
#=====================Create temp database which will be deleted later=============================#
arcpy.env.overwriteOutput =True
if not os.path.exists(r"C:\temp"):
    os.mkdir(r"C:\temp")
env.workspace = r"C:\temp"
arcpy.env.overwriteOutput =True
#=====================Declare local variables=============================#
fc = arcpy.GetParameterAsText(0)
wrkspace = arcpy.GetParameterAsText(1)
fc_out = arcpy.GetParameterAsText(2)
radius = arcpy.GetParameterAsText(3)

#=====================Declare constant local variables=============================#
distance = r"C:\temp\distance.dbf"


#spatial_ref = arcpy.Describe(fc).spatialReference.Name
prjs = arcpy.Describe(fc).spatialReference.exportToString()


#=================Do some analysis==========================#
arcpy.CreateFeatureclass_management(wrkspace,fc_out+".shp","POLYLINE",fc,"DISABLED","DISABLED",prjs)
arcpy.PointDistance_analysis(fc,fc,distance,radius)

#=================Create Pair of FID Points==========================#

curSDisnc = arcpy.SearchCursor(distance)

Inpt_FID = [row.getValue("INPUT_FID") for row in curSDisnc]
curSDisnc = arcpy.SearchCursor(distance)
Outpt_FID = [row.getValue("NEAR_FID") for row in curSDisnc]

pair = zip(Inpt_FID,Outpt_FID)

del curSDisnc

#============Insert Cursor=====================================#

curI = arcpy.da.InsertCursor(os.path.join(wrkspace,fc_out+".shp"), ["SHAPE@"])

 
#=====================Get X,Y data=============================#

curSfc = arcpy.da.SearchCursor(fc,["SHAPE@XY","FID"])


def retFID(X):
    sql = (""""FID" = {0}""").format(X)
    arcpy.AddMessage("Creating line for"+sql)
    cur= arcpy.da.SearchCursor(fc,["FID","SHAPE@XY"],sql)
    for i in cur:
        return i[1]
    del cur
#=====================Create polyine=============================#    
for m,n in pair:
    coordS = retFID(m)
    coordE = retFID(n)
    array = arcpy.Array([arcpy.Point(coordS[0], coordS[1]),arcpy.Point(coordE[0], coordE[1])])
    
    polyline = arcpy.Polyline(array)
    
    curI.insertRow([polyline])
    array.removeAll()            
del curI,curSfc
arcpy.Delete_management(distance)
try:
    shutil.rmtree(r"C:\temp")
except:
    pass

print "Completed Line Generation"

