import arcpy, os, fnmatch,pandas, numpy
preserve_input=r"D:\test_revise\preserve_input"
output=r"D:\test_revise\output_second"

def preserve_time(preserve_input, output):
    preserve_time_output=os.path.join(output,"preserve_time")
    if not os.path.exists(preserve_time_output):
        os.mkdir(preserve_time_output)
    else:
        pass

    build_output_path=os.path.join(preserve_time_output,"build")
    if not os.path.exists(build_output_path):
        os.mkdir(build_output_path)
    else:
        pass

    promote_output_path=os.path.join(preserve_time_output,"promote")
    if not os.path.exists(promote_output_path):
        os.mkdir(promote_output_path)
    else:
        pass

    preserve_file_lists=os.listdir(preserve_input)
    preserve_files=fnmatch.filter(preserve_file_lists,"*.shp")
    year_range=["0","1979","2000"]
    for file in preserve_files:
        preserve_file_name=file.split(".")[0]
        preserve_file_path=os.path.join(preserve_input,file)
        for y in range(len(year_range)):
            if y==2:
                expression_1="""{0}>{1}""".format(arcpy.AddFieldDelimiters(build_output_path,"Year"),year_range[y])
                expression_2="""{0}>{1}""".format(arcpy.AddFieldDelimiters(promote_output_path,"National_Y"),year_range[y])
                build_feature="{0}_{1}_{2}".format(year_range[y],"later","BuildTime")+".shp"
                build_feature_path=os.path.join(build_output_path,build_feature)

                promote_feature="{0}_{1}_{2}".format(year_range[y],"later","PromoteTime")+".shp"
                promote_feature_path=os.path.join(promote_output_path,promote_feature)

            else:
                expression_1="""{0}>{1} AND {2}<={3}""".format(arcpy.AddFieldDelimiters(build_output_path,"Year"),year_range[y],
                              arcpy.AddFieldDelimiters(build_output_path,"Year"),year_range[y+1])

                expression_2="""{0}>{1} AND {2}<={3}""".format(arcpy.AddFieldDelimiters(promote_output_path,"National_Y"),year_range[y],
                              arcpy.AddFieldDelimiters(promote_output_path,"National_Y"),year_range[y+1])
                                                  
                build_feature="{0}_{1}_{2}".format(year_range[y],year_range[y+1],"BuildTime")+".shp"
                build_feature_path=os.path.join(build_output_path,build_feature)


                promote_feature="{0}_{1}_{2}".format(year_range[y],year_range[y+1],"PromoteTime")+".shp"
                promote_feature_path=os.path.join(promote_output_path,promote_feature)

            arcpy.Select_analysis(preserve_file_path,build_feature_path,expression_1)
            arcpy.Select_analysis(preserve_file_path,promote_feature_path,expression_2)


preserve_time(preserve_input,output)
