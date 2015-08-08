import arcpy,os
arcpy.env.overwriteOutput = 1



tobe_updated = arcpy.GetParameterAsText(0)
count_feature = arcpy.GetParameterAsText(1)
count_field_name = arcpy.GetParameterAsText(2)
search_radius = arcpy.GetParameterAsText(3)

arcpy.AddMessage(tobe_updated)

arcpy.AddField_management(tobe_updated,count_field_name,"SHORT","10","#","#","#","NULLABLE","NON_REQUIRED","#")
pair = []
pairID = []
pairCNT = []
def getCount(fc,countFc,s_radius):
    arcpy.MakeFeatureLayer_management(fc,"sel_loc")
    arcpy.MakeFeatureLayer_management(countFc,"countF")
    curS = arcpy.da.SearchCursor("sel_loc",("OID@","SHAPE@"))
    for row in curS:
        S = row[1]
        arcpy.AddMessage("Searching By Location For: "+str(row[0]))
        arcpy.SelectLayerByLocation_management("countF","WITHIN_A_DISTANCE",S,s_radius,"NEW_SELECTION")
        cnt = str(arcpy.GetCount_management("countF"))
        pairID.append(row[0])
        pairCNT.append(cnt)
        pair.append(zip(pairID,pairCNT))      
    del curS
    return pair
getCount(tobe_updated, count_feature,search_radius)
arcpy.Delete_management("sel_loc")
arcpy.Delete_management("countF")
curU = arcpy.da.UpdateCursor(tobe_updated,("OID@",count_field_name))
for row in curU:
    for i in pair:
        for x,y in i:
            if (row[0] == x):
                row[1]= y
                curU.updateRow(row)
                arcpy.AddMessage("Completed Count For: "+ str(row[0]))
del curU


