import arcpy, os, numpy, csv, fnmatch, pandas
from arcpy import management
from collections import namedtuple

mammal_output=r"D:\test_revise\output\mammal"
bird_output=r"D:\test_revise\output\bird"
amphibian_output=r"D:\test_revise\output\amphibian"
preserve_area=r"D:\test_revise\output\preserve_area"
intersect=r"D:\test_revise\output\intersect"
root_folder=r"D:\test_revise\output"

def ToCSV(animal_output, preserve_output, intersect):
    #head=["Species range/NNR", "<10", ">100000", "10000-100000", "1000-10000", "100-1000", "10-100"]
    head=["File/NNR","1","2","3","4","5"]
    animal_folders=os.listdir(animal_output)
    animal_name=animal_folders[0]
    animal_type=animal_name.split("_")[0]
    intersect_animal=os.path.join(intersect,animal_type) #intersect\mammal
    if not os.path.exists(intersect_animal):
        os.mkdir(intersect_animal)
    #make a folder for summry tables:
    summary_folder=os.path.join(root_folder,"summary_dbf")
    if not os.path.exists(summary_folder):
        os.mkdir(summary_folder)
    summary_animal=os.path.join(summary_folder,animal_type)
    if not os.path.exists(summary_animal):
        os.mkdir(summary_animal)
    #print intersect_animal

    for animal_folder in animal_folders:
        animal_folder_path=os.path.join(animal_output,animal_folder) #output\mammal\mammal_china
        intersect_animal_type=os.path.join(intersect_animal,animal_folder)#intersect\mammal\mammal_china
        if not os.path.exists(intersect_animal_type):
            os.mkdir(intersect_animal_type)

        animal_lists=os.listdir(animal_folder_path)
        animals=fnmatch.filter(animal_lists,"*.shp")
        #print animals
        #print animal_folder_path
        #print intersect_animal_type


    preserve_types=os.listdir(preserve_output)
    #print preserve_types
    for preserve_type in preserve_types:
        preserve_type_path=os.path.join(preserve_output,preserve_type)
        #print preserve_type_path
        preserve_stages=os.listdir(preserve_type_path)
        #print preserve_stages

        for preserve_stage in preserve_stages:
            preserve_stage_path=os.path.join(preserve_type_path,preserve_stage)
            #print preserve_stage_path
            preserve_lists=os.listdir(preserve_stage_path)
            preserves=fnmatch.filter(preserve_lists,"*.shp")
            #print preserves

            count_list=list()
            percentage_list=list()
            count_list.append(head)
            percentage_list.append(head)
            

            for p in preserves:
                #print p
                p_name=p.split(".")[0]
                p_file_name="{0}_{1}_{2}".format(p_name.split("_")[2],p_name.split("_")[3],p_name.split("_")[4])
                p_path=os.path.join(preserve_stage_path,p)
                #print p_path
                p_row="{0}-{1}".format(p_name.split("_")[0],p_name.split("_")[1])
                count_row=list()
                percentage_row=list()
                count_row.append(p_row)
                percentage_row.append(p_row)

                for a in animals:
                    print a
                    a_path=os.path.join(animal_folder_path,a)
                    a_name=a.split(".")[0]
                    a_file_name="{0}_{1}".format(a_name.split("_")[2],a_name.split("_")[3])
                    intersect_features=[p_path,a_path]
                    out_intersect="{0}_{1}".format(a_name,p_name)+".shp"
                    out_intersect_path=os.path.join(intersect_animal_type,out_intersect)
                    arcpy.Intersect_analysis(intersect_features, out_intersect_path)

                    #Calculate geometric area of each patch
                    in_shp = out_intersect_path
                    features = "AREA"
                    Length_Unit = "KILOMETERS"
                    Area_Unit = "SQUARE_KILOMETERS"
                    arcpy.AddGeometryAttributes_management(in_shp, features, Length_Unit, Area_Unit)

                    #statistic, and get the dbf form
                    field="POLY_AREA"
                    field_1="Area_km2_1"
                    out_feature_class="{0}_{1}_{2}".format(a_name,p_name,"sta")+".dbf"
                    out_feature_class_path=os.path.join(summary_animal,out_feature_class)


                    arcpy.Statistics_analysis(in_shp,out_feature_class_path,[[field,"SUM"],[field_1,"MEAN"]], "binomial")
                    

                    #cauculate
                    #field="POLY_AREA"
                    #field_1="Area_km2_1"
                    #sum=0
                    #sum_1=0
                    #sum_percentage=0
                    #row=cursor.next()
                    
                    #Occurances=[]
                    with arcpy.da.SearchCursor(out_feature_class_path,["binomial","SUM_POLY_A","MEAN_Area_"]) as cursor:
                        percentage=0
                        Occurances=[]
                    
                        for row in cursor:
                            print row
                            Occurances.append(row[0])

                            try:
                                percent=row[1]/row[2]
                            except:
                                row[2]=0
                                percent=0

                            percentage=percentage+percent

                        final_number=len(Occurances)
                        print final_number
                        try:
                            final_percentage=percentage/final_number
                            print final_percentage
                        except:
                            final_number=0
                            final_percentage=0
                            print final_percentage

                        count_row.append(final_number)
                        percentage_row.append(final_percentage)
                        print count_row
                        print percentage_row
                    
                    #print a_name+"_"+p_name+" failed"
                count_list.append(count_row)
                percentage_list.append(percentage_row)
                print count_list
                print percentage_list
            
            output_csv=p_file_name+"_"+a_file_name+".csv"
            output_csv_root=os.path.join(root_folder,"tables")
            if not os.path.exists(output_csv_root):
                os.mkdir(output_csv_root)
            else:
                pass

            output_csv_animal=os.path.join(output_csv_root,animal_type)
            if not os.path.exists(output_csv_animal):
                os.mkdir(output_csv_animal)
            else:
                pass

            output_csv_number=os.path.join(output_csv_animal,"count")
            if not os.path.exists(output_csv_number):
                os.mkdir(output_csv_number)
            else:
                pass
            output_csv_path=os.path.join(output_csv_number,output_csv)
            with open(output_csv_path, "w") as output:
                writer = csv.writer(output, lineterminator='\n')
                writer.writerows(count_list)
                print "{} csv has been output".format(output_csv)



            output_per_csv=p_file_name+"_"+a_file_name+"_per"+".csv"

            output_csv_percentage=os.path.join(output_csv_animal,"percentage")
            if not os.path.exists(output_csv_percentage):
                os.mkdir(output_csv_percentage)
            else:
                pass
            output_csv_per_path=os.path.join(output_csv_percentage,output_per_csv)
            with open(output_csv_per_path, "w") as output:
                writer = csv.writer(output, lineterminator='\n')
                writer.writerows(percentage_list)
                print "{} csv has been output".format(output_per_csv)
                    
ToCSV(mammal_output, preserve_area, intersect)                    

