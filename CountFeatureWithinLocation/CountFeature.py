import arcpy
arcpy.env.overwriteOutput = True

inF = arcpy.GetParameterAsText(0)
selectF = arcpy.GetParameterAsText(1)
fName = arcpy.GetParameterAsText(2)

arcpy.env.workspace = r'C:\Users\USER_NAME\Desktop\gissta\workspace'
inF  = r'C:\Users\USER_NAME\Desktop\gissta\workspace\grid.shp'  #Practice_Stops
selectF = r'C:\Users\USER_NAME\Desktop\gissta\workspace\schools_p.shp'  # "Practice_Sales.shp"

pair = []
pairID = []
pairCNT = []

def getCount(fc,countFc):
    arcpy.MakeFeatureLayer_management(fc,"sel_loc")
    arcpy.MakeFeatureLayer_management(countFc,"countF")
    curS = arcpy.da.SearchCursor("sel_loc",("OID@","SHAPE@"))
    for row in curS:
        S = row[1]
        arcpy.SelectLayerByLocation_management("countF","WITHIN_A_DISTANCE",S,"1000 Meters","NEW_SELECTION")
        cnt = str(arcpy.GetCount_management("countF"))
        pairID.append(row[0])
        pairCNT.append(cnt)
        print zip(pairID,pairCNT)
        pair.append(zip(pairID,pairCNT))

    del curS
    return pair
getCount(inF, selectF)
curU = arcpy.da.UpdateCursor(inF,("OID@","COUNT"))
for row in curU:
    for i in pair:
        for x,y in i:
            print type(x)
            print type(row[0])
            print type(row[1])
            if (row[0] == x):
                row[1]= y
                curU.updateRow(row)
del curU