import arcpy, os, fnmatch, pandas, numpy,csv
preserve_input=r"D:\test_revise\preserve_input"
output=r"D:\test_revise\output"


def preserve(preserve_input, output):

    #select preserves based on time range:
    #build a list to store different type of year range
    preserve_time_output=os.path.join(output,"preserve_time")
    if not os.path.exists(preserve_time_output):
        os.mkdir(preserve_time_output)
    else:
        pass
    
    #year_type=["build","promote"]
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

    print build_output_path, promote_output_path
    

    #read input preserve file
    preserve_file_lists=os.listdir(preserve_input)
    preserve_files=fnmatch.filter(preserve_file_lists,"*.shp")
    year_range=["0","1979","2000"]
    for file in preserve_files:
        preserve_file_name=file.split(".")[0]
        print preserve_file_name
        preserve_file_path=os.path.join(preserve_input,file)
        for y in range(len(year_range)):
            if y==2:
                print year_range[y]
                expression_1="""{0}>{1}""".format(arcpy.AddFieldDelimiters(build_output_path,"Year"),year_range[y])
                expression_2="""{0}>{1}""".format(arcpy.AddFieldDelimiters(promote_output_path,"National_Y"),year_range[y])
                build_feature="{0}_{1}_{2}".format(year_range[y],"later","BuildTime")+".shp"
                build_feature_path=os.path.join(build_output_path,build_feature)

                promote_feature="{0}_{1}_{2}".format(year_range[y],"later","PromoteTime")+".shp"
                promote_feature_path=os.path.join(promote_output_path,promote_feature)

            else:
                print year_range[y]
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


    preserve_area_range=["0","10","100","1000","10000","100000","1000000"]
    #build folder to preserve all preserve area outputs
    preserve_area=os.path.join(output,"preserve_area")
    if not os.path.exists(preserve_area):
        os.mkdir(preserve_area)
    else:
        pass


    #read files in preserve_time
    preserve_area_input_folders=os.listdir(preserve_time_output) #build, promote
    print preserve_area_input_folders

    for folder in preserve_area_input_folders:

        preserve_area_input_fo=os.path.join(preserve_time_output,folder) #preserve_time\build, promote
        preserve_area_input_lists=os.listdir(preserve_area_input_fo) #0-1979, 1979-2000, 2000-2018
        preserve_area_inputs=fnmatch.filter(preserve_area_input_lists,"*.shp") 
        print preserve_area_inputs


        preserve_area_stage=os.path.join(preserve_area,folder)
        if not os.path.exists(preserve_area_stage):
            os.mkdir(preserve_area_stage) #preserve_area\(build, promote)


        for file in preserve_area_inputs:
            preserve_area_input_name=file.split(".")[0]
            preserve_area_input_path=os.path.join(preserve_area_input_fo,file) #preserve_time\build, promote\file

            #define output path:
            preserve_area_output_path=os.path.join(preserve_area_stage,preserve_area_input_name)
            if not os.path.exists(preserve_area_output_path):
                os.mkdir(preserve_area_output_path)


            for a in range(len(preserve_area_range)):
                if a==6:
                    print preserve_area_range[a]
                    expression="""{0}>{1}""".format(arcpy.AddFieldDelimiters(preserve_area_output_path,"Area_km2"),preserve_area_range[a])
                    print expression
                    output_feature="{0}_{1}_{2}".format(preserve_area_range[a],"higher",preserve_area_input_name)+".shp"
                    output_feature_path=os.path.join(preserve_area_output_path,output_feature)

                else:
                    print preserve_area_range[a]
                    expression="""{0}>{1} AND {2}<={3}""".format(arcpy.AddFieldDelimiters(preserve_area_output_path,"Area_km2"),
                                                                 preserve_area_range[a],arcpy.AddFieldDelimiters(preserve_area_output_path,"Area_km2"),
                                                                 preserve_area_range[a+1])
                    output_feature="{0}_{1}_{2}".format(preserve_area_range[a],preserve_area_range[a+1],preserve_area_input_name)+".shp"
                    output_feature_path=os.path.join(preserve_area_output_path,output_feature)
                arcpy.Select_analysis(preserve_area_input_path,output_feature_path,expression)


preserve(preserve_input,output)
