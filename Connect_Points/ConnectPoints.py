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
fc = arcpy.GetParameterAsText(0)#r'C:\Users\Winrock\Documents\ArcGIS\snp_early.shp'
fc_out = arcpy.GetParameterAsText(1)#r'C:\Users\Winrock\Documents\ArcGIS\snp_early_lines.shp'
radius = arcpy.GetParameterAsText(2)#"1000 Meters"
#radius = "{0} Meters".format(radius)

#=====================Declare constant local variables=============================#
distance = r"C:\temp\distance.dbf"


#spatial_ref = arcpy.Describe(fc).spatialReference.Name
prjs = arcpy.Describe(fc).spatialReference.exportToString()


#=================Do some analysis==========================#
arcpy.CreateFeatureclass_management(out_path=os.path.dirname(fc_out), out_name=os.path.basename(fc_out), geometry_type="POLYLINE", template="", has_m="DISABLED", has_z="DISABLED", spatial_reference=prjs, config_keyword="", spatial_grid_1="0", spatial_grid_2="0", spatial_grid_3="0")
arcpy.PointDistance_analysis(fc,fc,distance,radius)

#=================Create Pair of FID Points==========================#
curSDisnc = arcpy.da.SearchCursor(distance,("INPUT_FID","NEAR_FID"))
Inpt_FID = [row[0] for row in curSDisnc]
curSDisnc = arcpy.da.SearchCursor(distance,("INPUT_FID","NEAR_FID"))
Outpt_FID = [row[1] for row in curSDisnc]
pair = zip(Inpt_FID,Outpt_FID)
del curSDisnc

#============Insert Cursor=====================================#

curI = arcpy.da.InsertCursor(os.path.join(fc_out), ["SHAPE@"])

 
#=====================Get X,Y data=============================#
objid = [i.name for i in arcpy.ListFields(fc)][0]
curSfc = arcpy.da.SearchCursor(fc,["SHAPE@XY",objid])


def retFID(X):
    sql = ("""{0} = {1}""").format(objid,X)
    arcpy.AddMessage("Creating line for"+sql)
    cur= arcpy.da.SearchCursor(fc,[objid,"SHAPE@XY"],sql)
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