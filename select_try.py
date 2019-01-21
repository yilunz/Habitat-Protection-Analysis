import arcpy, os
#input_data=r"D:\test_revise\mammal_input\mammal_world_clip.shp"
input_data=r"D:\test_revise\bird_input\bird_world_clip.shp"
#output=r"D:\test_revise\output\mammal"
output=r"D:\test_revise\output\bird"
for t in range(0,2013):
    output_feature="{0}_{1}".format(t,"bird_world")+".shp"
    output_path=os.path.join(output,output_feature)
    where_clause= """{0}={1}""".format(arcpy.AddFieldDelimiters(input_data,"FID"),t)
               
#where_clause = '"FID" = 53'
    arcpy.Select_analysis(input_data,output_path,where_clause)
