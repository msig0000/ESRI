#!/usr/bin/python
# -*- #################
#Author:Shariful Islam
#Contact: msi_g@yahoo.com

'''
This tool copies data from one feature class(updater feature class) to another 

feature class(input feature class) using common field between them.
'''

import arcpy,os,time,ast,re
from collections import defaultdict


data = defaultdict(set)


#############################INPUT###########################################################################




input_fc=(                            arcpy.GetParameterAsText(0)
#r"C:\Users\Winrock\Desktop\taco\Project.gdb\PW_StreetMaintenance_ServiceRequest_1"
)


common_field_updating=(              arcpy.GetParameterAsText(1)
#'INCIDENT_NUMBER'
)


updating_fields_tmp= (                arcpy.GetParameterAsText(2)
#'CLOSE_DATE'
)



updating_fields = [updating_fields_tmp,common_field_updating]





updater_fc = (                       arcpy.GetParameterAsText(3)
#r"C:\Users\Winrock\Desktop\taco\Project.gdb\CRMMasterFeatureClass"
)

common_field_updater =(            arcpy.GetParameterAsText(4)
#'INCIDENT_NUMBER'
)

updater_fields_tmp =(                arcpy.GetParameterAsText(5)
#'CLOSE_DATE'
)


updater_fields = [updater_fields_tmp,common_field_updater]






#############################INPUT###########################################################################



#generate comons
conatiner_common_updating = []
conatiner_common_updater = []
with arcpy.da.SearchCursor(input_fc,updating_fields) as in_fc_cur:
  for row_in in in_fc_cur:
    conatiner_common_updating.append(row_in[-1]) 
with arcpy.da.SearchCursor(updater_fc,updater_fields) as mapp_fc_cur:
  for row_updt in mapp_fc_cur:
    conatiner_common_updater.append(row_updt[-1])  
tmp = set(conatiner_common_updating).intersection(set(conatiner_common_updater))
unqs = list(i.encode('utf-8') if isinstance(i,unicode) else i for i in tmp)


#Set Progressor for data dictionary generation
arcpy.AddMessage("\n\nGetting common attributes. Wait!!...")
arcpy.SetProgressor('step',"Getting common attributes from   {0}  .........".format(os.path.basename(updater_fc)),0,len(conatiner_common_updater),1)


#generate data dict
with arcpy.da.SearchCursor(updater_fc,updater_fields) as mapp_fc:
    for row_s in mapp_fc:
      if row_s[-1] in unqs:
        data[row_s[-1]].add(row_s[0])
      arcpy.SetProgressorLabel("Getting attribute from {0} .....".format(os.path.basename(input_fc)))
      arcpy.SetProgressorPosition()
#arcpy.ResetProgressor()        
                        

#Set Progressor for feature updating
arcpy.SetProgressor('step',"Updating  {0}  .........".format(os.path.basename(input_fc)),0,len(unqs),1)
arcpy.AddMessage("\n\nFound {0} common rows between {1}  and  {2}.\n\n".format(len(unqs),os.path.basename(input_fc),os.path.basename(updater_fc)))
arcpy.AddMessage("Updating {0}...".format(os.path.basename(input_fc)))
#time.sleep(5)

#Update

with arcpy.da.UpdateCursor(input_fc,updating_fields) as in_fc:
        for row_u in in_fc:
          if row_u[-1] in unqs:
            if data[row_u[-1]]:
              row_u[0]=data[row_u[-1]].pop()
          in_fc.updateRow(row_u)
          arcpy.SetProgressorLabel("Updating {0}   {1}  of   {2} .....".format(common_field_updater,row_u[-1],os.path.basename(input_fc)))
          arcpy.SetProgressorPosition()
          #time.sleep(.001)
arcpy.ResetProgressor()
arcpy.AddMessage("All Done!!!")


