import arcpy, os, fnmatch,pandas, numpy
amphibian_input=r"D:\test_revise\amphibian_input"
mammal_input=r"D:\test_revise\output\mammal"
bird_input=r"D:\test_revise\output\bird"
output=r"D:\test_revise\output_second"
preserve_time=r"D:\test_revise\output_second\preserve_time"

def intersect_2(animal_input, output):
    #animal_name=animal
    #animal_type=animal_input.split("_")[1]
    #print animal_type

    ####Build dbf output root folder####
    summary_folder_1=os.path.join(output,"summary_dbf_1")
    if not os.path.exists(summary_folder_1):
        os.mkdir(summary_folder_1)
    #summary_animal_1=os.path.join(summary_folder_1,animal_type)
    #print summary_animal_1
    #if not os.path.exists(summary_animal_1):
        #os.mkdir(summary_animal_1)

    animal_file_lists=os.listdir(animal_input)
    animal_files=fnmatch.filter(animal_file_lists,"*.shp")
    #print animal_files
    
        #animal_file_name=abunak
        #animal_output=os.path.join(output,
    for a in animal_files:
        a_name=a.split(".")[0]
        a_type=a_name.split("_")[1]
        print a_type
        a_path=os.path.join(animal_input,a)

        ####Under output root folder, build animal name folder for shp files, eg. output-->mammal####
        animal_output_path=os.path.join(output,a_type)
        if not os.path.exists(animal_output_path):
            os.mkdir(animal_output_path)
        else:
            pass

        ####Under animal name folder, build seperate folders for each fild, eg. output-->mammal-->0_mammal_world####
        a_output_path=os.path.join(animal_output_path,a_name)
        if not os.path.exists(a_output_path):
            os.mkdir(a_output_path)
        else:
            pass
        print a_output_path

        ####Under dbf output root folder, build animal name folder, eg. summary_dbf-->mammal####
        dbf_path=os.path.join(summary_folder_1,a_type)
        if not os.path.exists(dbf_path):
            os.mkdir(dbf_path)
        else:
            pass

        
        time_folders=os.listdir(preserve_time)
        #print time_folders

        for time_folder in time_folders:
            time_folder_path=os.path.join(preserve_time,time_folder)
            #print time_folder_path

            ####Under animal name folder, build folder for each time period, eg. summary_dbf-->mammal-->build####
            period_path=os.path.join(dbf_path,time_folder)
            if not os.path.exists(period_path):
                os.mkdir(period_path)
            else:
                pass

            time_file_lists=os.listdir(time_folder_path)

            #time_files_lists=os.listdir(time_folder)
            time_files=fnmatch.filter(time_file_lists,"*.shp")
            #print time_files

            

            for t in time_files:
                t_name=t.split(".")[0]
                t_path=os.path.join(time_folder_path,t)
                ####Under period folder, build time range folder, eg. summary_dbf-->mammal-->build-->1979####
                timeRange_path=os.path.join(period_path,t_name)
                if not os.path.exists(timeRange_path):
                    os.mkdir(timeRange_path)
                else:
                    pass
                print timeRange_path

                #a_t_file_name="{0}_{1}".format(a_name.split("_")[2],a_name.split("_")[3])
                intersect_features=[a_path,t_path]
                out_inter="{0}_{1}".format(a_name,t_name)+".shp"
                out_inter_path=os.path.join(a_output_path,out_inter)
                arcpy.Intersect_analysis(intersect_features, out_inter_path)


                #Calculate geometric area of each patch
                input_shp= out_inter_path
                features = "AREA"
                Length_Unit = "KILOMETERS"
                Area_Unit = "SQUARE_KILOMETERS"
                arcpy.AddGeometryAttributes_management(input_shp, features, Length_Unit, Area_Unit)
    

                #statistic, and get the dbf form
                field="Poly_Area"
                field_1="Area_km2"
                out_feature_class="{0}_{1}_{2}".format(a_name,t_name,"sta")+".dbf"
                out_feature_class_path=os.path.join(timeRange_path,out_feature_class)

                arcpy.Statistics_analysis(input_shp,out_feature_class_path,[[field,"SUM"],[field_1,"MEAN"]], "SCINAME")
                

                
               

intersect_2(bird_input,output)   
