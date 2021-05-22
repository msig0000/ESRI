import arcpy
import pythonaddins as pa

arcpy.env.overwriteOutput = True

# InFC = r'C:\Users\pc\OneDrive\Documents\ArcGIS\Default.gdb\test_point'
# SerialField = u'MyOrder' #arcpy.Describe(InFC).OIDFieldName
# DistancField = u'Distance'

InFC = arcpy.GetParameterAsText(0)
SerialField = arcpy.GetParameterAsText(1)
DistancField = arcpy.GetParameterAsText(2)

arcpy.AddMessage("Adding cumulative distance field, namely, {0} to the feature {1} based on the order as set by serial or oder field named {2}".\
    format(DistancField,InFC,SerialField))

features = [f for f in arcpy.da.SearchCursor(InFC, (SerialField, "SHAPE@"),
                                             sql_clause=(None, "ORDER BY {0} ASC".format(SerialField)))]
desc = arcpy.Describe(InFC)
update_values = []

if desc.shapeType == u'Polyline':
    length = 0.0
    for index, f in enumerate(features):
        if index < len(features):
            length += f[1].length
            update_values.append((f[0], length))
elif desc.shapeType == u'Point':
    length = 0.0
    update_values.append((0, length))
    for index, f in enumerate(features):
        if index < len(features) - 1:
            length += features[index][1].distanceTo(features[index + 1][1])
            update_values.append((f[0], length))

# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view
# within the script The following inputs are layers or table views: "Sample_Points_ConnectPoints"
if DistancField not in [ff_.name for ff_ in arcpy.ListFields(InFC)]:
    arcpy.AddField_management(in_table=InFC, field_name=DistancField, field_type="DOUBLE", field_precision="10",
                              field_scale="10", field_length="", field_alias="", field_is_nullable="NULLABLE",
                              field_is_required="NON_REQUIRED", field_domain="")
elif pa.MessageBox('Field with name {} already exits do you want to delete it and create new one?'.format(DistancField),'Do you want to proceed?',3):
    arcpy.DeleteField_management(InFC,
                                 [DistancField])
    arcpy.AddField_management(in_table=InFC, field_name=DistancField, field_type="DOUBLE", field_precision="10",
                              field_scale="10", field_length="", field_alias="", field_is_nullable="NULLABLE",
                              field_is_required="NON_REQUIRED", field_domain="")

with arcpy.da.UpdateCursor(InFC, (DistancField, SerialField),
                           sql_clause=(None, "ORDER BY {0} ASC".format(SerialField))) as upd_cur:
    for index, row in enumerate(upd_cur):
        row[0] = update_values[index][1]
        upd_cur.updateRow(row)