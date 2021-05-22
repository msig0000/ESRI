import arcpy
import Tkinter as tk
from tkinter import messagebox as mb

root = tk.Tk()
root.withdraw()

arcpy.env.overwriteOutput = True

# InFC = r'C:\Users\pc\OneDrive\Documents\ArcGIS\Default.gdb\test_point'  # 'Sample_Points_ConnectPoints  '  # arcpy.GetParameterAsText(0)
# SerialField = arcpy.Describe(InFC).OIDFieldName  # 'OBJECTID'  # u'Unq'  # arcpy.GetParameterAsText(1)
# DistancField = u'LengthC1'  # arcpy.GetParameterAsText(2)


InFC = arcpy.GetParameterAsText(0)
SerialField = arcpy.GetParameterAsText(1)
DistancField = arcpy.GetParameterAsText(2)

arcpy.AddMessage(InFC)
arcpy.AddMessage(SerialField)
arcpy.AddMessage(DistancField)

def messagebox(title, message, **options):
    res = mb.askquestion(title, message)
    if res == 'yes':
        return True
    else:
        # mb.showinfo('Return', 'Returning to main application')
        return False


features = [f for f in arcpy.da.SearchCursor(InFC, (SerialField, "SHAPE@"),
                                             sql_clause=(None, "ORDER BY '{0}'".format(SerialField)))]
desc = arcpy.Describe(InFC)
update_values = []

if desc.shapeType == u'Polyline':
    length = features[0][1].length
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
elif messagebox('Do you want to proceed?', 'Field with this name exits do you want to delete it and create new one?'):
    arcpy.DeleteField_management(InFC,
                                 [DistancField])
    arcpy.AddField_management(in_table=InFC, field_name=DistancField, field_type="DOUBLE", field_precision="10",
                              field_scale="10", field_length="", field_alias="", field_is_nullable="NULLABLE",
                              field_is_required="NON_REQUIRED", field_domain="")

with arcpy.da.UpdateCursor(InFC, (DistancField, SerialField),
                           sql_clause=(None, "ORDER BY '{0}'".format(SerialField))) as upd_cur:
    for index, row in enumerate(upd_cur):
        row[0] = update_values[index][1]
        upd_cur.updateRow(row)
