import arcpy
arcpy.env.overwriteOutput = True

InFC = arcpy.GetParameterAsText(0)
UnqField = arcpy.GetParameterAsText(1)
DistancField = arcpy.GetParameterAsText(2)

features = [f for f in arcpy.da.SearchCursor(InFC,(UnqField,"SHAPE@"),
                                             sql_clause=(None,"ORDER BY UnqField"))]

index = 1
length = 0
update_values = [(0,0)]
for f in features:
    if index < len(features):
        length += f[1].distanceTo(features[index][1])
        index += 1
        update_values.append((f[0],length))
    else:
        pass

with arcpy.da.UpdateCursor(InFC,(DistancField,UnqField),sql_clause=(None,"ORDER BY UnqField")) as upd_cur:
    index = 0
    for row in upd_cur:
        row[0] = update_values[index][1]
        upd_cur.updateRow(row)
        index += 1
